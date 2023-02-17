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

class ImportCont(db.Model):
    __tablename__ = "import_ref_cont"
    
    import_ref_n = db.Column(db.Integer, primary_key=True, nullable=False)
    cont_n = db.Column(db.String, primary_key=True, nullable=False)

    def __init__(self, import_ref_n, cont_n):
        self.import_ref_n = import_ref_n
        self.cont_n = cont_n

    def json(self):
        return {
            "import_ref_n": self.import_ref_n,
            "cont_n": self.cont_n
        }

# Retrieve IMPORT_REF_N from IMPORT_REF_CONT by CONT_N
@app.route("/import_cont/import_ref_n", methods=['POST'])
def get_import_ref_n():
    data = request.get_json()
    container_number = data["container_number"]
    import_ref_n = ImportCont.query.filter_by(cont_n=container_number).first().import_ref_n
    
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

# Retrieve CONT_N from IMPORT_REF_CONT using IMPORT_REF_N (NOT ABLE TO GET ALL VALUES ONLY THE FIRST VALUE RETRIEVED)
@app.route("/import_cont/<int:import_ref_n>", methods=['GET'])
def get_cont_num(import_ref_n):
    try:
        container_nums = ImportCont.query.filter_by(import_ref_n = import_ref_n).all()
        
        if len(container_nums):
            container_numbers = [{"container_num": cont.cont_n} for cont in container_nums]
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "container_nums": container_numbers
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
    app.run(host='0.0.0.0', port=8087, debug=True)