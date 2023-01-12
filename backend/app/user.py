from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.exc import IntegrityError

import hashlib
import shortuuid
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "oracle://wg:wgdemo*()@202.73.56.175:1521/efprod" # TODO: Externalise into env config file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# with app.app_context():    
#     user = db.Table('WG_USER', db.metadata, autoload=True, autoload_with=db.engine)
# db.Model.metadata.reflect(bind=db.engine,schema='WG')

class User(db.Model):
    __tablename__ = "wg_user"

    wguser_id = db.Column(db.String, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password_salt = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer)
    company = db.Column(db.String)

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

@app.route("/user/signup", methods=['POST'])
def sign_up():

    json_payload = request.get_json()
    username = json_payload['username']
    email = json_payload['email']
    phone = json_payload['phone']
    company = json_payload['company']
    password = json_payload['password']

    if validate_username(username) is not None:
        return validate_username(username)

    password_salt = uuid.uuid4().hex
    password_hash = hashlib.sha512(
        password.encode('utf-8') + password_salt.encode('utf-8')
    ).hexdigest()

    new_user = User(username, email, password_salt, password_hash, phone, company)

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
    username_given = True
    try:
        json_payload = request.get_json()
        input_password = json_payload['password']

        if '@' in json_payload['username']:
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
                "message": "user not found",
            }), 404

        input_password_hash = hashlib.sha512(
            input_password.encode('utf-8') + found_user.password_salt.encode('utf-8')
        ).hexdigest()
        verified = found_user.password_hash == input_password_hash

        if not verified:
            return jsonify({
                "code": 401,
                "message": "wrong password"
            }), 401
        
        return jsonify({
            "code": 200,
            "message": "login success",
        }), 200

    except Exception as err:
        return jsonify({
            "code": 500,
            "message": "Failed to login",
            "data": str(err)
        }), 500

if __name__ == "__main__":
    app.run(debug=True) # debug for DEV environment only