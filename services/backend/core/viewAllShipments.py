# NOT ABLE TO INSTALL INVOKES ON MY END CAN SOMEONE HELP ME INSTALL AND TRY THIS OUT? all the other 4 services works individually

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http

from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Service Classes
IMPORT_URL = "http://localhost:8085"
IMPORT_CONT_URL = "http://localhost:8087"

EXPORT_URL = "http://localhost:8086"
EXPORT_CONT_URL = "http://localhost:8088"

@app.route("/getExportContainerNum", methods=['POST'])
def getExportContainerNum():

    data = request.get_json()
    wguser_id = data['wguser_id']

    export_ref_num_response = invoke_http(EXPORT_URL + "/export/export_ref_n/wguser_id" + str(wguser_id), method='GET')
    export_ref_num = export_ref_num_response['export_ref_n']

    cont_num_response = invoke_http(EXPORT_CONT_URL + "/export_cont/cont_num" + int(export_ref_num), method='GET')
    cont_num = cont_num_response['container_num']

    if cont_num:
        return jsonify(
            {
                "code":200,
                "data":
                {
                    "container_num" : cont_num

                }
            }
        ),200
    
    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve container number"
        }
    ), 500

@app.route("/getImportContainerNum", methods=['POST'])
def getImportContainerNum():

    data = request.get_json()
    wguser_id = data['wguser_id']

    import_ref_num_response = invoke_http(IMPORT_URL + "/import/import_ref_n/wguser_id/" + str(wguser_id), method='GET')
    import_ref_num = import_ref_num_response['export_ref_n']

    cont_num_response = invoke_http(IMPORT_CONT_URL + "/import_cont/cont_num/" + int(import_ref_num), method='GET')
    cont_num = cont_num_response['container_num']

    if cont_num:
        return jsonify(
            {
                "code":200,
                "data":
                {
                    "container_num" : cont_num

                }
            }
        ),200
    
    return jsonify(
        {
            "code": 500,
            "message": "Failed to retrieve container number"
        }
    ), 500






if __name__ == "__main__":
    app.run(port=8089, debug=True)