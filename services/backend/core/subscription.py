import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from os import getenv
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Subscription(db.Model):
    __tablename__ = "subscription"
    
    subscription_id = db.Column(db.Integer, primary_key=True, nullable=False)
    wguser_id = db.Column(db.String, nullable=False)
    container_id = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=True)

    def __init__(self, wguser_id, container_id, status):
      
        self.container_id = container_id
        self.status = status
        self.wguser_id = wguser_id
        

    def json(self):
        return {
           
            "container_id": self.container_id,
            "status": self.status,
            "wguser_id": self.wguser_id
        }

# Retrieve IMPORT_REF_N by House B/L
@app.route("/subscription/add", methods=['POST'])
def insert_subscription():
    data = request.get_json()
    user_id = data["userid"]
    containerid=data["containerid"]
    status=data["status"]
    new_subscription = Subscription(user_id,containerid,status)

    try:
        db.session.add(new_subscription)
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "New Subscription to Notification added"
        }), 201
    except IntegrityError as err1:
        return jsonify({
            "code": 500,
            "message": "Duplicate subscription",
            "data": str(err1)
        }), 500
    except Exception as err:
        return jsonify({
            "code": 500,
            "message": "Subscription unsuccessful",
            "data": str(err)
        }), 500

@app.route("/subscription/getsubscriptions", methods=['POST'])
def getsubscriptions():
    
    
    # try:
        vendor_name = Subscription.query.all()
        arr=[]
        for row in vendor_name:
            data={
                "subscription_id":row.subscription_id,
                "wguser_id":row.wguser_id,
                "container_id":row.container_id,
                "status":row.status
            }
            arr.append(data)
        return arr
       

        

        # if vendor_name:
        #     return jsonify(
        #         {
        #         "code": 200,
        #         "data": vendor_name
        #         }
        #     ), 200
    
    # except:
    #     return jsonify(
    #         {
    #             "code": 404,
    #             "message": "No Records!"
    #         }
    #     ), 404
@app.route("/ping", methods=['GET'])
def health_check():
    return("import")
  
# Retrieve IMPORT_REF_N using WGUSER_ID -> Returning all the IMPORT_REF_N according to WGUSER_ID and sorted by latest to earliest using DELIVERY_D
@app.route("/subscription/delete", methods=['POST'])
def deleteuser():
    
        data = request.get_json()
        containerid = data['containerid']
        subscription = Subscription.query.filter_by(container_id=containerid).first()
       
        try:
             db.session.delete(subscription)
             db.session.commit()
             return jsonify({
                "code": 201,
                "message": " Subscription removed "
            }), 201
       
        except Exception as err:
            return jsonify({
                "code": 500,
                "message": "Subscription removal unsuccessful",
                "data": str(err)
            }), 500

@app.route("/subscription/update", methods=['POST'])
def updateuser():
    
        data = request.get_json()
        containerid = data['containerid']
        status=data["status"]
        subscription = Subscription.query.filter_by(container_id=containerid).first()
        subscription.status=status
       
        try:
             db.session.commit()
             return jsonify({
                "code": 201,
                "message": " status updated "
            }), 201
       
        except Exception as err:
            return jsonify({
                "code": 500,
                "message": "Subscription status update unsuccessful",
                "data": str(err)
            }), 500

      
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5013, debug=True)
    # app.run(host='0.0.0.0', debug=True)
