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

class ExportCont(db.Model):
    __tablename__ = "export_ref_cont"
    
    export_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    cont_n = db.Column(db.String, primary_key=True, nullable=False)

    def __init__(self, export_ref_n, cont_n):
        self.export_ref_n = export_ref_n
        self.cont_n = cont_n

    def json(self):
        return {
            "export_ref_n": self.export_ref_n,
            "cont_n": self.cont_n
        }

# Retrieve EXPORT_REF_N from EXPORT_REF_CONT by CONT_N
@app.route("/export_cont/export_ref_n", methods=['POST'])
def get_export_ref_n():
    data = request.get_json()
    container_number = data["container_number"]
    export_ref_n = ExportCont.query.filter_by(cont_n=container_number).first().export_ref_n
    
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

# Retrieve CONT_N from EXPORT_REF_CONT using EXPORT_REF_N --> Returns a List which will be appended to the response from export.py function
@app.route("/export_cont/container_num", methods=['POST'])
def get_cont_num():
    try:
        data = request.get_json()
        export_ref_n = data["export_ref_n"]
        container_nums = ExportCont.query.filter_by(export_ref_n = export_ref_n).all()
        # print(containerList)

        
        if len(container_nums):
            outputList = []
            for container_num in container_nums:
                outputList.append(container_num.cont_n)
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "container_nums": outputList
                    }
                }
            ), 200

    
    except Exception as e:
        return jsonify(
            {
                "code":500,
                "message":"Failed to retrieve container_num because : " + str(e)
            }
        ), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5007, debug=True)
    # app.run(host='0.0.0.0', debug=True)

"""
Sample API Endpoint

http://127.0.0.1:5007/export_cont/container_num

Sample JSON request

{
    "export_ref_n" : 17587
}

Sample JSON response

{
    "code": 200,
    "data": {
        "container_nums": [
            "REGU4985177",
            "REGU4995920",
            "REGU4991740",
            "REGU4205368",
            "TEXU7407574",
            "CRXU4483116",
            "TEXU7099492",
            "REGU4982408"
        ]
    }
}

"""