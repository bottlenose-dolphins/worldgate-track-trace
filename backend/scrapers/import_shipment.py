from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ImportShipment(db.Model):
    __tablename__ = "import_ref"

    import_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    eta = db.Column(db.Date, nullable=False)
    ocean_bl = db.Column(db.String, nullable=False)

    def __init__(self, import_ref_n, eta, ocean_bl):
        self.import_ref_n = import_ref_n
        self.eta = eta
        self.ocean_bl = ocean_bl

    def json(self):
        return {
            "import_ref_n": self.import_ref_n,
            "eta": self.eta,
            "ocean_bl": self.ocean_bl
        }

# Retrieve shipment information by Master B/L
@app.route("/import_shipment/retrieve", methods=['POST'])
def retrieve_shipment():
    data = request.get_json()
    master_bl = data["master_bl"]
    response = ImportShipment.query.filter_by(ocean_bl=master_bl).first()
    
    if response:
        return jsonify(
                {
                "code": 200,
                "data": {
                    "import_ref_n": response.import_ref_n,
                    "eta": response.eta
                    }
                }
            ), 200
    
    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve shipment information"
        }
    ), 500

# Retrieve Master B/L by IMPORT_REF_N
@app.route("/import_shipment/bl", methods=['POST'])
def get_master_bl():
    data = request.get_json()
    import_ref_n = data["import_ref_n"]
    master_bl = ImportShipment.query.filter_by(import_ref_n=import_ref_n).first().ocean_bl
    
    if master_bl:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "master_bl": master_bl
                    }
            }
        ), 200
    
    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve Master B/L no."
        }
    ), 500

# Update latest shipment information
@app.route("/import_shipment/update", methods=['POST'])
def update_shipment():
    data = request.get_json()
    eta = data["arrival_date"]
    vessel_name = data["vessel_name"]
    master_bl = data["master_bl"]

    shipment = ImportShipment.query.filter_by(ocean_bl=master_bl).first()
    
    if shipment:
        shipment.eta = eta
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": {
                    "eta": eta
                    }
            }
        ), 200

    return jsonify(
        {
            "code": 500,
            "message": "Failed to update shipment information"
        }
    ), 500

if __name__ == "__main__":
    app.run(port=8083, debug=True)