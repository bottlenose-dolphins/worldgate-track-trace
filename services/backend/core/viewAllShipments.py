from flask import Flask, jsonify, request
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http
from flask_cors import CORS

from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# to include in dockerfile
prod = getenv('prod')

db = SQLAlchemy(app)

# Service Classes
IMPORT_URL = "http://core_import:5003"
IMPORT_CONT_URL = "http://core_import_cont:5004"

EXPORT_URL = "http://core_export:5006"
EXPORT_CONT_URL = "http://core_export_cont:5007"


@app.route("/getExportContainerNum", methods=['POST'])
def getExportContainerNum():

    data = request.get_json()
    wguser_id = data['wguser_id']

    data = {
                "wguser_id" : wguser_id
            }

    export_ref_num_response = invoke_http(EXPORT_URL + "/export/export_ref_n/wguser_id", method="POST", json=data)
    export_ref_num_dumped = json.dumps(export_ref_num_response)
    export_ref_num_loads = json.loads(export_ref_num_dumped)
    export_ref_num = export_ref_num_loads['data']['export_ref_n']

    data = {
                "export_ref_n" : export_ref_num
            }

    container_num_response = invoke_http(EXPORT_CONT_URL + "/export_cont/container_num", method="POST", json=data)
    container_num_response_dumped = json.dumps(container_num_response)
    container_num_response_loads = json.loads(container_num_response_dumped)

    return container_num_response_loads



@app.route("/getImportContainerNum", methods=['POST'])
def getImportContainerNum():

    data = request.get_json()
    wguser_id = data['wguser_id']

    data = {
                "wguser_id" : wguser_id
            }

    import_ref_num_response = invoke_http(IMPORT_URL + "/import/import_ref_n/wguser_id", method="POST", json=data)
    import_ref_num_dumped = json.dumps(import_ref_num_response)
    import_ref_num_response_loads = json.loads(import_ref_num_dumped)
    import_ref_num = import_ref_num_response_loads['data']['import_ref_n']

    data = {
                "import_ref_n" : import_ref_num
            }

    container_num_response = invoke_http(IMPORT_CONT_URL + "/import_cont/container_num", method="POST", json=data)
    container_num_response_dumped = json.dumps(container_num_response)
    container_num_response_loads = json.loads(container_num_response_dumped)

    return container_num_response_loads

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
    # app.run(host='0.0.0.0', debug=True)
