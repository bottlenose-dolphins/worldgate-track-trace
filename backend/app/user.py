from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "oracle://wg:wgdemo*()@202.73.56.175:1521/efprod"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
with app.app_context():    
    user = db.Table('WG_USER', db.metadata, autoload=True, autoload_with=db.engine)
# db.Model.metadata.reflect(bind=db.engine,schema='WG')

# class User(db.Model):
#   __tablename__ = "WGUser"

#   email = db.Column(db.String(255), primary_key=True)
#   name = db.Column(db.String(255), nullable=False)
#   password = db.Column(db.String(255), nullable=False)

#   def __init__(self, email, name, password_hash):
#     self.email = email
#     self.name = name
#     self.password = password_hash

#   def json(self):
#     return {
#         "email": self.email,
#         "name": self.name,
#         "password": self.password,
#     }

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
            found_user = db.session.query(user).filter_by(username=input_username).first()
        else:
            found_user = db.session.query(user).filter_by(email=input_email).first()
        if found_user is None:
            return jsonify({
                "code": 404,
                "message": "user not found",
            }), 404
        verified = found_user.user_password == input_password
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
    app.run(debug=True)