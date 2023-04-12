from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://www.worldgatetracktrace.click", "http://127.0.0.1", "http://worldgatetracktrace.click", "localhost"]}})

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Import(db.Model):
    __tablename__ = "import"
    
    import_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    cust_id = db.Column(db.String, nullable=False)
    hbl_n = db.Column(db.String, nullable=False)
    wguser_id = db.Column(db.String, nullable=True)
    delivery_d = db.Column(db.Date, nullable=True)

    def __init__(self, import_ref_n, cust_id, hbl_n, wguser_id):
        self.import_ref_n = import_ref_n
        self.cust_id = cust_id
        self.hbl_n = hbl_n
        self.wguser_id = wguser_id

    def json(self):
        return {
            "import_ref_n": self.import_ref_n,
            "cust_id": self.cust_id,
            "hbl_n": self.hbl_n,
            "wguser_id": self.wguser_id
        }

# Retrieve IMPORT_REF_N by House B/L
@app.route("/import/import_ref_n", methods=['POST'])
def get_import_ref_n():
    data = request.get_json()
    house_bl = data["house_bl"]
    import_ref_n = Import.query.filter_by(hbl_n=house_bl).first().import_ref_n
    
    if import_ref_n:
        return jsonify(
                {
                "code": 200,
                "data": {
                    "import_ref_n": import_ref_n
                    }
                }
            ), 200

    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve import_ref_n"
        }
    ), 500

# Retrieve House B/L by IMPORT_REF_N
@app.route("/import/hbl", methods=['POST'])
def get_hbl():
    data = request.get_json()
    import_ref_n = data["import_ref_n"]
    hbl_n = Import.query.filter_by(import_ref_n=import_ref_n).first().hbl_n
    
    if hbl_n:
        return jsonify(
                {
                "code": 200,
                "data": {
                    "hbl": hbl_n
                    }
                }
            ), 200

    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve hbl_n"
        }
    ), 500

@app.route("/ping", methods=['GET'])
def health_check():
    return("import")
  
# Retrieve IMPORT_REF_N using WGUSER_ID -> Returning all the IMPORT_REF_N according to WGUSER_ID and sorted by latest to earliest using DELIVERY_D
@app.route("/import/import_ref_n/wguser_id", methods=['POST'])
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
    # app.run(host='0.0.0.0', port=5003, debug=True)
    app.run(host='0.0.0.0', debug=True)

"""
SAMPLE API ENDPOINT

http://127.0.0.1:5003/import/import_ref_n/wguser_id

SAMPLE JSON REQUEST

{
    "wguser_id" : "HMuAqcsAFtnJGfrM84VqL7"
}

SAMPLE OUTPUT

[
    {
        "container_numbers": [
            "HLXU5027876",
            "HLXU2139717",
            "HLCU4187010",
            "HLCU2231582",
            "HLCU2258177",
            "HLXU3075047",
            "HLCU2100704"
        ],
        "delivery_date": "01/06/2021",
        "export_destination": "KARACHI",
        "export_ref_n": 17612,
        "type": "Export"
    },
    {
        "container_numbers": [
            "GESU4205066",
            "HDMU6127648",
            "TGHU7584650"
        ],
        "delivery_date": "07/11/2020",
        "export_destination": "MUMBAI,INDIA",
        "export_ref_n": 17625,
        "type": "Export"
    },
    {
        "container_numbers": [
            "COPU5223250",
            "COPU4226315"
        ],
        "delivery_date": "05/09/2017",
        "export_destination": "CHITTAGONG",
        "export_ref_n": 17595,
        "type": "Export"
    },
    {
        "container_numbers": [
            "DNAU2559042",
            "DNAU2514140",
            "DNAU2517113",
            "DNAU2334827",
            "DNAU2404837",
            "DNAU2528566"
        ],
        "delivery_date": "27/05/2017",
        "export_destination": "HAMBURG",
        "export_ref_n": 17648,
        "type": "Export"
    },
    {
        "container_numbers": [
            "COKU0020043",
            "XTRU2060428",
            "UXXU2229503"
        ],
        "delivery_date": "12/06/2010",
        "export_destination": "CHIASSO CY",
        "export_ref_n": 17581,
        "type": "Export"
    },
    {
        "container_numbers": [
            "EMCU 3424530",
            "IPXU 3371140",
            "FSCU 7532318",
            "FSCU 7840795"
        ],
        "delivery_date": "19/11/2009",
        "export_destination": "BANGKOK PORT, *",
        "export_ref_n": 17633,
        "type": "Export"
    },
    {
        "container_numbers": [
            "REGU4985177",
            "REGU4995920",
            "REGU4991740",
            "REGU4205368",
            "TEXU7407574",
            "CRXU4483116",
            "TEXU7099492",
            "REGU4982408"
        ],
        "delivery_date": "23/09/2005",
        "export_destination": "CHIASSO CY",
        "export_ref_n": 17587,
        "type": "Export"
    },
    {
        "container_numbers": [
            "YMLU 4947640",
            "YMLU 4494327",
            "YMLU 4933266"
        ],
        "delivery_date": "08/05/1999",
        "export_destination": "NHAVA SHEVA",
        "export_ref_n": 17549,
        "type": "Export"
    },
    {
        "container_numbers": [
            "CLHU3395117",
            "ZCSU8202585",
            "GLDU7038020"
        ],
        "delivery_date": "22/09/1997",
        "export_destination": "NHAVA SHEVA",
        "export_ref_n": 17609,
        "type": "Export"
    }
]
"""    



