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

class Export(db.Model):
    __tablename__ = "export"
    
    export_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    cust_id = db.Column(db.String, nullable=False)
    hbl_n = db.Column(db.String, nullable=False)
    wguser_id = db.Column(db.String, nullable=False)
    port_del_name = db.Column(db.String, nullable=False)
    del_to = db.Column(db.Date, nullable=False)

    def __init__(self, export_ref_n, cust_id, hbl_n, wguser_id, port_del_name, del_to):
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
    data = request.get_json()
    wguser_id = data["wguser_id"]
    output = Export.query.filter_by(wguser_id=wguser_id).order_by(Export.del_to.desc()).all()

    if len(output):
        result = [
            {
                "export_ref_n": a_row.export_ref_n,
                "destination_port": a_row.port_del_name,
                "delivery_date": a_row.del_to
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


    
    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve export_ref_n"
        }
    ), 500

@app.route("/ping", methods=['GET'])
def health_check():
    return("Hi")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006, debug=True)
    # app.run(host='0.0.0.0', debug=True)

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
                "delivery_date": "Tue, 01 Jun 2021 00:00:00 GMT",
                "destination_port": "KARACHI",
                "export_ref_n": 14368
            },
            {
                "delivery_date": "Sat, 07 Nov 2020 00:00:00 GMT",
                "destination_port": "MUMBAI,INDIA",
                "export_ref_n": 14165
            },
            {
                "delivery_date": "Tue, 05 Sep 2017 00:00:00 GMT",
                "destination_port": "CHITTAGONG",
                "export_ref_n": 14284
            },
            {
                "delivery_date": "Sat, 27 May 2017 00:00:00 GMT",
                "destination_port": "HAMBURG",
                "export_ref_n": 14161
            },
            {
                "delivery_date": "Sat, 12 Jun 2010 00:00:00 GMT",
                "destination_port": "CHIASSO CY",
                "export_ref_n": 14290
            },
            {
                "delivery_date": "Thu, 19 Nov 2009 00:00:00 GMT",
                "destination_port": "BANGKOK PORT, *",
                "export_ref_n": 14166
            },
            {
                "delivery_date": "Fri, 23 Sep 2005 00:00:00 GMT",
                "destination_port": "CHIASSO CY",
                "export_ref_n": 17587
            },
            {
                "delivery_date": "Sun, 07 Nov 1999 00:00:00 GMT",
                "destination_port": "COLOMBO, SRI LANKA",
                "export_ref_n": 14277
            },
            {
                "delivery_date": "Sat, 08 May 1999 00:00:00 GMT",
                "destination_port": "NHAVA SHEVA",
                "export_ref_n": 14520
            }
        ]
    }
}
"""



