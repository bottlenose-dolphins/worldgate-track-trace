from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://worldgatetracktrace.click, http://127.0.0.1"}})

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Vendor(db.Model):
    __tablename__ = "vendor_mast"

    vendor_id = db.Column(db.String, primary_key=True, nullable=False)
    vendor_name = db.Column(db.String, nullable=False)

    def __init__(self, vendor_id, vendor_name):
        self.vendor_id = vendor_id
        self.vendor_name = vendor_name

    def json(self):
        return {
            "vendor_id": self.vendor_id,
            "vendor_name": self.vendor_name
        }

@app.route("/ping", methods=['GET'])
def health_check():
    return("vendor_mast")

# Retrieve vendor_name by vendor_id
@app.route("/vendor_mast/vendor_name", methods=['POST'])
def get_vendor_name():
    data = request.get_json()
    vendor_id = data["vendor_id"]
    try:
        vendor_name = Vendor.query.filter_by(vendor_id=vendor_id).first().vendor_name

        if vendor_name:
            return jsonify(
                {
                "code": 200,
                "data": {
                    "vendor_name": vendor_name
                    }
                }
            ), 200
    
    except:
        return jsonify(
            {
                "code": 404,
                "message": "This vendor does not exist!"
            }
        ), 404

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5012, debug=True)
    app.run(host='0.0.0.0', debug=True)