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

class ExportShipment(db.Model):
    __tablename__ = "export_ref"

    export_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    eta = db.Column(db.Date, nullable=False)
    ocean_bl = db.Column(db.String, nullable=False)
    port_disc_id = db.Column(db.String, nullable=False)

    def __init__(self, export_ref_n, eta, ocean_bl, port_disc_id):
        self.export_ref_n = export_ref_n
        self.eta = eta
        self.ocean_bl = ocean_bl
        self.port_disc_id = port_disc_id

    def json(self):
        return {
            "export_ref_n": self.export_ref_n,
            "eta": self.eta,
            "ocean_bl": self.ocean_bl,
            "port_disc_id": self.port_disc_id
        }

# Retrieve shipment information by Master B/L
@app.route("/export_shipment/retrieve", methods=['POST'])
def retrieve_shipment():
    data = request.get_json()
    master_bl = data["master_bl"]
    response = ExportShipment.query.filter_by(ocean_bl=master_bl).first()
    
    if response:
        return jsonify(
                {
                "code": 200,
                "data": {
                    "export_ref_n": response.export_ref_n,
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

# Retrieve Master B/L by EXPORT_REF_N
@app.route("/export_shipment/bl", methods=['POST'])
def get_master_bl():
    data = request.get_json()
    export_ref_n = data["export_ref_n"]
    master_bl = ExportShipment.query.filter_by(export_ref_n=export_ref_n).first().ocean_bl
    
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
@app.route("/export_shipment/update", methods=['POST'])
def update_shipment():
    data = request.get_json()
    eta = data["arrival_date"]
    port_of_discharge = data["port_of_discharge"]
    vessel_name = data["vessel_name"]
    master_bl = data["master_bl"]

    shipment = ExportShipment.query.filter_by(ocean_bl=master_bl).first()
    
    if shipment:
        shipment.eta = eta
        shipment.port_disc_id = port_of_discharge
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "data": {
                    "eta": eta,
                    "port_disc_id": port_of_discharge
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