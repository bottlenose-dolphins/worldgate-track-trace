from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Export(db.Model):
    __tablename__ = "export"
    
    export_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    cust_id = db.Column(db.String, nullable=False)
    hbl_n = db.Column(db.String, nullable=False)
    wguser_id = db.Column(db.String, nullable=False)
    port_del_name = db.Column(db.String, nullable=False)

    def __init__(self, export_ref_n, cust_id, hbl_n, wguser_id, port_del_name):
        self.export_ref_n = export_ref_n
        self.cust_id = cust_id
        self.hbl_n = hbl_n
        self.wguser_id = wguser_id
        self.port_del_name = port_del_name

    def json(self):
        return {
            "export_ref_n": self.export_ref_n,
            "cust_id": self.cust_id,
            "hbl_n": self.hbl_n,
            "wguser_id": self.wguser_id,
            "port_del_name": self.port_del_name
        }

@app.route("/ping", methods=['GET'])
def health_check():
    return("export")

# Retrieve EXPORT_REF_N by House B/L
@app.route("/export/export_ref_n", methods=['POST'])
def get_export_ref_n():
    data = request.get_json()
    house_bl = data["house_bl"]
    export_ref_n = Export.query.filter_by(hbl_n=house_bl).first().export_ref_n
    
    if export_ref_n:
        return jsonify(
                {
                "code": 200,
                "data": {
                    "export_ref_n": export_ref_n
                    }
                }
            ), 200

    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve export_ref_n"
        }
    ), 500

# Retrieve EXPORT_REF_N, PORT_DEL_NAME and DEL_TO using WGUSER_ID and sorted in descending order using DEL_TO
@app.route("/export/export_ref_n/wguser_id", methods=['POST'])
def get_export_ref_n_using_wguser_id():
    try:
        data = request.get_json()
        wguser_id = data["wguser_id"]
        output = Export.query.filter_by(wguser_id=wguser_id).all()

        if len(output):
            result = [
                    {
                        "export_ref_n": a_row.export_ref_n,
                        "export_destination": a_row.port_del_name,
                        "type": "export"
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
    # app.run(host='0.0.0.0', port=5006, debug=True)
    app.run(host='0.0.0.0', debug=True)

"""
    SAMPLE API ENDPOINT

    http://127.0.0.1:5006/export/export_ref_n/wguser_id

    SAMPLE JSON REQUEST

    {
        "wguser_id" : "bk666dcoeZTH3dxZCuu4FR"
    }

    SAMPLE OUTPUT

    {
    "code": 200,
    "data": {
        "output": [
            {
                "delivery_date": "01/06/2021",
                "export_destination": "KARACHI",
                "export_ref_n": 17612,
                "type": "Export"
            },
            {
                "delivery_date": "07/11/2020",
                "export_destination": "MUMBAI,INDIA",
                "export_ref_n": 17625,
                "type": "Export"
            },
            {
                "delivery_date": "05/09/2017",
                "export_destination": "CHITTAGONG",
                "export_ref_n": 17595,
                "type": "Export"
            },
            {
                "delivery_date": "27/05/2017",
                "export_destination": "HAMBURG",
                "export_ref_n": 17648,
                "type": "Export"
            },
            {
                "delivery_date": "12/06/2010",
                "export_destination": "CHIASSO CY",
                "export_ref_n": 17581,
                "type": "Export"
            },
            {
                "delivery_date": "19/11/2009",
                "export_destination": "BANGKOK PORT, *",
                "export_ref_n": 17633,
                "type": "Export"
            },
            {
                "delivery_date": "23/09/2005",
                "export_destination": "CHIASSO CY",
                "export_ref_n": 17587,
                "type": "Export"
            },
            {
                "delivery_date": "08/05/1999",
                "export_destination": "NHAVA SHEVA",
                "export_ref_n": 17549,
                "type": "Export"
            },
            {
                "delivery_date": "22/09/1997",
                "export_destination": "NHAVA SHEVA",
                "export_ref_n": 17609,
                "type": "Export"
            }
        ]
    }
}
"""



