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

class Prefix(db.Model):
    __tablename__ = "bl_mapping"

    shipping_acronym = db.Column(db.String, primary_key=True, nullable=False)
    shipping_fullform = db.Column(db.String, nullable=False)

    def __init__(self, shipping_acronym, shipping_fullform):
        self.shipping_acronym = shipping_acronym
        self.shipping_fullform = shipping_fullform

    def json(self):
        return {
            "shipping_acronym": self.shipping_acronym,
            "shipping_fullform": self.shipping_fullform
        }

# Check if prefix exists
def prefix_exists(shipping_line):
    prefix = Prefix.query.filter_by(shipping_fullform=shipping_line)
    if prefix:
        return True
    return False

# Retrieve prefix
@app.route("/prefix/retrieve", methods=['POST'])
def retrieve_prefix():
    data = request.get_json()
    shipping_line = data["shipping_line"]
    if prefix_exists(shipping_line):
        prefix = Prefix.query.filter_by(shipping_fullform=shipping_line).first().shipping_acronym

        if prefix:
            return jsonify(
                {
                "code": 200,
                "data": {
                    "prefix": prefix
                    }
                }
            ), 200
    
    return jsonify(
        {
            "code": 404,
            "message": "This shipping line does not have an existing prefix!"
        }
    ), 404

# Add prefix
@app.route("/prefix/add", methods=['POST'])
def add_prefix(prefix, shipping_line):
    if not prefix_exists(shipping_line):
        new_prefix = Prefix(prefix, shipping_line)
        
        try:
            db.session.add(new_prefix)
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "message": "Add prefix success"
                }
            ), 201
        except Exception as err:
            return jsonify(
                {
                    "code": 500,
                    "message": "Add prefix unsuccessful: " + str(err)
                }
            ), 500
    
    return jsonify(
        {
            "code": 409,
            "message": "A prefix already exists for this shipping line!",
        }
    ), 409

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5011, debug=True)
    # app.run(host='0.0.0.0', debug=True)
