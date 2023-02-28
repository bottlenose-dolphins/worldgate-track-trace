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

class Import(db.Model):
    __tablename__ = "import"
    
    import_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    cust_id = db.Column(db.String, nullable=False)
    hbl_n = db.Column(db.String, nullable=False)
    wguser_id = db.Column(db.String, nullable=True)
    delivery_d = db.Column(db.Date, nullable=True)

    def __init__(self, import_ref_n, cust_id, hbl_n, wguser_id, delivery_d):
        self.import_ref_n = import_ref_n
        self.cust_id = cust_id
        self.hbl_n = hbl_n
        self.wguser_id = wguser_id
        self.delivery_d = delivery_d

    def json(self):
        return {
            "import_ref_n": self.import_ref_n,
            "cust_id": self.cust_id,
            "hbl_n": self.hbl_n,
            "wguser_id": self.wguser_id,
            "delivery_d": self.delivery_d
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

# Retrieve IMPORT_REF_N using WGUSER_ID -> Returning all the IMPORT_REF_N according to WGUSER_ID and sorted by latest to earliest using DELIVERY_D
@app.route("/import/import_ref_n/wguser_id", methods=['POST'])
def get_import_ref_n_using_wguser_id():
    data = request.get_json()
    wguser_id = data['wguser_id']
    output = Import.query.filter_by(wguser_id=wguser_id).order_by(Import.delivery_d.desc()).all()

    if len(output):
        result = [
                {
                    "import_ref_n": a_row.import_ref_n,
                    "import_destination": "Singapore",
                    "arrival_date": str(a_row.delivery_d),
                    "type": "Import"
                }
        for a_row in output]

        for a_record in result:
            date_str = a_record["arrival_date"]
            dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date_str = dt_obj.strftime('%d/%m/%Y')
            a_record["arrival_date"] = formatted_date_str

            
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
            "message": "Failed to retrieve import_ref_n"
        }
    ), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)
    # app.run(host='0.0.0.0', debug=True)

"""
SAMPLE API ENDPOINT

http://127.0.0.1:5003/import/import_ref_n/wguser_id

SAMPLE JSON REQUEST

{
    "wguser_id" : "HMuAqcsAFtnJGfrM84VqL7"
}

SAMPLE OUTPUT

{
    "code": 200,
    "data": {
        "output": [
            {
                "arrival_date": "Thu, 22 Sep 2022 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14100
            },
            {
                "arrival_date": "Sun, 30 Jun 2019 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14057
            },
            {
                "arrival_date": "Fri, 02 Nov 2018 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14019
            },
            {
                "arrival_date": "Sat, 16 Jul 2016 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14059
            },
            {
                "arrival_date": "Fri, 27 Jun 2014 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14073
            },
            {
                "arrival_date": "Sat, 26 Jun 2004 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14238
            },
            {
                "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14114
            },
            {
                "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14115
            },
            {
                "arrival_date": "Thu, 10 Jun 2004 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14069
            },
            {
                "arrival_date": "Tue, 08 Jun 2004 00:00:00 GMT",
                "import_destination": "Singapore",
                "import_ref_n": 14058
            }
        ]
    }
}
"""    



