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
def get_import_ref_n_using_wguser_id():
    try:
        data = request.get_json()
        wguser_id = data['wguser_id']
        output = Import.query.filter_by(wguser_id=wguser_id).all()

        if len(output):
            result = [
                    {
                        "import_ref_n": a_row.import_ref_n,
                        "import_destination": "Singapore",
                        "type": "import"
                    }
            for a_row in output]

            return jsonify(
                {
                    "code":200,
                    "data":
                    {
                        "output" : result
                    }
                }
            ),200
        
        else:
            return jsonify(
                {
                    "code":200,
                    "data":
                    {
                        "output" : "No details retrieved with the wguser_id : " + wguser_id
                    }
                }
            ),200

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Failed to retrieve shipment information: " + str(e)
            }
        ), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5013, debug=True)
    # app.run(host='0.0.0.0', debug=True)
