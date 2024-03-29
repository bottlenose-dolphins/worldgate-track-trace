from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, jwt_required
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import cx_Oracle
from obtainIp import obtainIP

from os import getenv
from dotenv import load_dotenv

import hashlib
import re
import shortuuid
import uuid

# cx_Oracle.init_oracle_client(lib_dir=r"D:\oracle\instantclient_21_8") #point this to your local installation of the oracle DB files

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, expose_headers="Set-Cookie")

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = getenv(
    'JWT_SECRET', default='secret_local_testing_only')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# app.config['JWT_COOKIE_SECURE'] = True # for prod

jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "wg_user"

    wguser_id = db.Column(db.String, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password_salt = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, default=None)
    company = db.Column(db.String, default=None)

    def __init__(self, username, email, password_salt, password_hash, phone, company):
        self.wguser_id = generate_uuid()
        self.username = username
        self.email = email
        self.password_salt = password_salt
        self.password_hash = password_hash
        self.phone = phone
        self.company = company

    def json(self):
        return {
            "wguser_id": self.wguser_id,
            "username": self.username,
            "email": self.email,
            "password_salt": self.password_hash,
            "password_hash": self.password_hash,
            "phone": self.phone,
            "company": self.company
        }


def validate_username(username):
    existing_user_username = User.query.filter_by(username=username).first()
    if existing_user_username:
        return jsonify({
            "code": 401,
            "message": "username already taken"
        }), 404
    return None


def generate_uuid():
    return shortuuid.uuid()


def is_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False


@app.route("/ping", methods=['GET'])
def health_check():
    return("user")    

@app.route("/user/signup", methods=['POST'])
def sign_up():
    """
    :param: { email: <str:email>, name: <str:name>, password: <str:password> , phone: <int:phone>, company: <str:company> }
    :return: { message: <str:message> }
    :rtype: json string
    """

    json_payload = request.get_json()
    username = json_payload['username']
    email = json_payload['email']
    password = json_payload['password']
    phone = json_payload['phone']
    company = json_payload['company']

    if validate_username(username) is not None:
        return validate_username(username)

    password_salt = uuid.uuid4().hex
    password_hash = hashlib.sha512(
        password.encode('utf-8') + password_salt.encode('utf-8')
    ).hexdigest()

    new_user = User(username, email, password_salt,
                    password_hash, phone, company)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Create user success"
        }), 201
    except IntegrityError as err1:
        return jsonify({
            "code": 500,
            "message": "Duplicate entry",
            "data": str(err1)
        }), 500
    except Exception as err:
        return jsonify({
            "code": 500,
            "message": "Create user unsuccessful",
            "data": str(err)
        }), 500


@app.route("/user/signin", methods=['POST'])
def sign_in():
    """
    :param: { username: <str:username/email>, password: <str:password> }
    :return: { message: <str:message> }
    :rtype: json string
    """
    username_given = True
    try:
        json_payload = request.get_json()
        input_password = json_payload['password']

        if is_email(json_payload['username']):
            input_email = json_payload['username']
            username_given = False
        else:
            input_username = json_payload['username']

        if username_given:
            found_user = User.query.filter_by(username=input_username).first()
        else:
            found_user = User.query.filter_by(email=input_email).first()

        if found_user is None:
            return jsonify({
                "code": 404,
                "message": "User not found",
            }), 404

        input_password_hash = hashlib.sha512(
            input_password.encode('utf-8') +
            found_user.password_salt.encode('utf-8')
        ).hexdigest()
        verified = found_user.password_hash == input_password_hash

        if not verified:
            return jsonify({
                "code": 401,
                "message": "Wrong password"
            }), 401

        # access token stored in httpOnly cookie,
        # double submit token stored in regular cookie
        additional_claims = {"username": found_user.username}
        access_token = create_access_token(
            identity=found_user.wguser_id, additional_claims=additional_claims)

        response = jsonify({
            "code": 200,
            "message": "login success",
            "username": found_user.username
        })
        set_access_cookies(response, access_token)
        return response

    except Exception as err:
        return jsonify({
            "code": 500,
            "message": "Error: Failed to login",
            "data": str(err)
        }), 500


@app.route("/user/signout", methods=["POST"])
def sign_out():
    response = jsonify({
        "code": 200,
        "message": "sign out successful"})
    unset_jwt_cookies(response)
    return response, 200

# Using an `after_request` callback, we refresh any token that is within 15 minutes of expiring.


@app.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


"""
To be called before ALL protected endpoints. Verifies valid JWT and double submit token in request header
Returns username and wguser_id of user.
"""


@app.route("/user/verify", methods=['GET'])
@jwt_required()
def verify_jwt_csrf_validity():
    # decode jwt to extract the csrf
    csrf_in_jwt = get_jwt()["csrf"]
    csrfHeader = request.headers.get('X-CSRF-TOKEN')
    print("csrfJWT : " + csrf_in_jwt)
    print("csrfHeader : " + csrfHeader)
    if csrf_in_jwt is None or request.headers.get('X-CSRF-TOKEN') is None: # no cookie or request header
        return jsonify({
            "code": 500,
            "message": "Token Not Found - Request Unauthorised"
        }), 500
    # get csrf token in header
    csrf_in_header = request.headers.get('X-CSRF-TOKEN').split(' ')[-1]
    # compare both csrfs
    if csrf_in_jwt != csrf_in_header:
        print("crsf dont match")
        return jsonify({
            "code": 500,
            "message": "Invalid Token - Request Unauthorised"
        }), 500
    else:
        claims = get_jwt()
        return jsonify({
            "code": 200,
            "message": "Valid Request",
            "userId": get_jwt_identity(),  # wguser_id
            "username": claims["username"]
        })

@app.route("/user/getnumber", methods=['POST'])
def get_number():
    data = request.get_json()
    userid = data["wguserid"]
    try:
        phone = User.query.filter_by(wguser_id=userid).first().phone

        if phone:
            return str(phone)
    except:
        return jsonify(
            {
                "code": 404,
                "message": "This user does not exist!"
            }
        ), 404

    # decode jwt to extract the csrf
   


if __name__ == "__main__":
    #app.run(debug=True)
     app.run(host='0.0.0.0', port=5002, debug=True) #to work as a local flask app
