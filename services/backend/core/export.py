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

    def __init__(self, export_ref_n, cust_id, hbl_n, wguser_id):
        self.export_ref_n = export_ref_n
        self.cust_id = cust_id
        self.hbl_n = hbl_n
        self.wguser_id = wguser_id

    def json(self):
        return {
            "export_ref_n": self.export_ref_n,
            "cust_id": self.cust_id,
            "hbl_n": self.hbl_n,
            "wguser_id": self.wguser_id
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

# Retrieve EXPORT_REF_N using WGUSER_ID
@app.route("/export/export_ref_n/wguser_id", methods=['POST'])
def get_export_ref_n_using_wguser_id():
    data = request.get_json()
    wguser_id = data["wguser_id"]
    export_ref_n = Export.query.filter_by(wguser_id=wguser_id).first().export_ref_n

    if export_ref_n:
        return jsonify(
            {
                "code":200,
                "data":
                {
                    "export_ref_n" : export_ref_n

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
    app.run(host='0.0.0.0', port=8086, debug=True)
    # app.run(host='0.0.0.0', debug=True)
