from datetime import datetime
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
    cr_agent_id = db.Column(db.String, nullable=False)
    og_eta = db.Column(db.Date, nullable=False)
    job_type = db.Column(db.String, nullable=False)
    cont_released = db.Column(db.DateTime, nullable=False)
    del_taken = db.Column(db.DateTime, nullable=False)

    def __init__(self, export_ref_n, eta, ocean_bl, port_disc_id, cr_agent_id, og_eta, job_type, cont_released, del_taken):
        self.export_ref_n = export_ref_n
        self.eta = eta
        self.ocean_bl = ocean_bl
        self.port_disc_id = port_disc_id
        self.cr_agent_id = cr_agent_id
        self.og_eta = og_eta
        self.job_type = job_type
        self.cont_released = cont_released
        self.del_taken = del_taken

    def json(self):
        return {
            "export_ref_n": self.export_ref_n,
            "eta": self.eta,
            "ocean_bl": self.ocean_bl,
            "port_disc_id": self.port_disc_id,
            "cr_agent_id": self.cr_agent_id,
            "og_eta": self.og_eta,
            "job_type": self.job_type,
            "cont_released": self.cont_released,
            "del_taken": self.del_taken
        }

@app.route("/ping", methods=['GET'])
def health_check():
    return("export_shipment")

# Retrieve shipment job type (FCL or LCL), cont_released and del_taken by Master B/L
@app.route("/export_shipment/cont_status", methods=['POST'])
def retrieve_cont_status():
    data = request.get_json()
    master_bl = data["master_bl"]
    response = ExportShipment.query.filter_by(ocean_bl=master_bl).first()

    if response:
        return jsonify(
                {
                "code": 200,
                "data": {
                    "export_ref_n": response.export_ref_n,
                    "master_bl": master_bl,
                    "job_type": response.job_type,
                    "cont_released": response.cont_released,
                    "del_taken": response.del_taken
                    }
                }
            ), 200
    
    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve container status"
        }
    ), 500

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

# Retrieve ETA by EXPORT_REF_N
@app.route("/export_shipment/retrieve_export_ref_n", methods=['POST'])
def retrieve_shipment_export_ref_n():
    data = request.get_json()
    export_ref_n = data["export_ref_n"]
    response = ExportShipment.query.filter_by(export_ref_n=export_ref_n).first()
    
    if response:
        return jsonify(
                {
                "code": 200,
                "data": {
                    "eta": response.eta.strftime("%Y/%m/%d")
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

# Update latest shipment information (BL)
@app.route("/export_shipment/update", methods=['POST'])
def update_shipment():
    data = request.get_json()
    eta = datetime.strptime(data["arrival_date"].replace("-","/"), '%Y/%m/%d')
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
            "message": "Failed to update shipment information (BL)"
        }
    ), 500

# Update latest shipment information (CONTAINER)
@app.route("/export_shipment/update_cont", methods=['POST'])
def update_shipment_cont():
    data = request.get_json()
    export_ref_n = data["export_ref_n"]
    eta = datetime.strptime(data["arrival_date"].replace("-","/"), '%Y/%m/%d')
    port_of_discharge = data["port_of_discharge"]
    vessel_name = data["vessel_name"]

    shipment = ExportShipment.query.filter_by(export_ref_n=export_ref_n).first()

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
            "message": "Failed to update shipment information (CONTAINER)"
        }
    ), 500

# Retrieve cr_agent_id by ocean_bl
@app.route("/export_shipment/agent_id", methods=['POST'])
def get_agent_id():
    data = request.get_json()
    master_bl = data["master_bl"]
    
    try:
        cr_agent_id = ExportShipment.query.filter_by(ocean_bl=master_bl).first().cr_agent_id

        if cr_agent_id:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "cr_agent_id": cr_agent_id
                        }
                }
            ), 200
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "Failed to retrieve CR_AGENT_ID"
            }
        ), 500

# Retrieve delay status by export_ref_n
@app.route("/export_shipment/delay", methods=['POST'])
def get_delay_status():
    data = request.get_json()
    export_ref_n = data["export_ref_n"]
    
    try:
        eta = ExportShipment.query.filter_by(export_ref_n=export_ref_n).first().eta
        og_eta = ExportShipment.query.filter_by(export_ref_n=export_ref_n).first().og_eta

        if eta > og_eta:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "status": "delayed"
                        }
                }
            ), 200
        elif eta == og_eta:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "status": "on time"
                        }
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "status": "early"
                        }
                }
            ), 200
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "Failed to retrieve delay status"
            }
        ), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008, debug=True)
    # app.run(host='0.0.0.0', debug=True)
