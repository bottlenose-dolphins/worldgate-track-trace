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
    cont_n = db.Column(db.String, nullable=False)

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

if __name__ == "__main__":
    app.run(port=8088, debug=True)