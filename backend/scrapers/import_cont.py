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
    cont_n = db.Column(db.String, nullable=False)

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

if __name__ == "__main__":
    app.run(port=8087, debug=True)