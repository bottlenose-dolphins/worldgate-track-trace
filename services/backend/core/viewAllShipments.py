# NOT ABLE TO INSTALL INVOKES ON MY END CAN SOMEONE HELP ME INSTALL AND TRY THIS OUT? all the other 4 services works individually

from flask import Flask, jsonify, request
import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
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

db = SQLAlchemy(app)

# Service Classes
IMPORT_URL = "http://localhost:8085"
IMPORT_CONT_URL = "http://localhost:8087"

EXPORT_URL = "http://localhost:8086"
EXPORT_CONT_URL = "http://localhost:8088"

# session = requests.Session()
# retry = Retry(connect=3, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# session.mount('http://', adapter)
# session.mount('https://', adapter)

@app.route("/getExportContainerNum", methods=['POST'])
def getExportContainerNum():

    data = request.get_json()
    wguser_id = data['wguser_id']

    export_ref_num_response = invoke_http(EXPORT_URL + "/export/export_ref_n/wguser_id" + str(wguser_id), method='GET')
    export_ref_num = export_ref_num_response['export_ref_n']

    cont_num_response = invoke_http(EXPORT_CONT_URL + "/export_cont/cont_num" + str(export_ref_num), method='GET')
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
    print("helloooooo")
    data = request.get_json()
    wguser_id = data['wguser_id']
    print(wguser_id)

    # url = "http://localhost:8085"

    # import_ref_num_response = invoke_http(IMPORT_URL + "/import/import_ref_n/" + str(wguser_id), method='GET')
    data = {
                "wguser_id" : "HMuAqcsAFtnJGfrM84VqL7"
            }

    import_ref_num_response = invoke_http("http://127.0.0.1:8085/import/import_ref_n/HMuAqcsAFtnJGfrM84VqL7", method="POST", json=data)
    # url = IMPORT_URL + "/import/import_ref_n/" + str(wguser_id)
    # requests.get(url)
    import_ref_num_response_dumped = json.dumps(import_ref_num_response)
    # parsed_import_ref_num = json.loads(import_ref_num_response)
    # import_ref_n = import_ref_num_response[0][0]

    print(import_ref_num_response_dumped)

    print("byebyebye")

    # if import_ref_num_response == None:
    #     return jsonify(
    #     {
    #         "code": 500,
    #         "message": "issa null"
    #     }
    # ), 500

    # else:
    #     return jsonify(
    #         {
    #             "code":200,
    #             "data":
    #             {
    #                 "container_num" : import_ref_num_response

    #             }
    #         }
    #     ),200
    
    return import_ref_num_response_dumped


        # if isinstance(parsed_import_ref_num, list):

        #     if 'data' in parsed_import_ref_num[0]:
        #         import_ref_n = parsed_import_ref_num[0]['data'].get('import_ref_n', None)

        #         if import_ref_n is not None:
        #             print(import_ref_n)

        #         else:
        #             print("Key 'import_ref_n' not found in the 'data' object.")

        #     else:
        #         print("Key 'data' not found in the parsed JSON.")

        # elif isinstance(parsed_import_ref_num, dict):

        #     if 'data' in parsed_import_ref_num:
        #         import_ref_n = parsed_import_ref_num['data'].get('import_ref_n', None)

        #         if import_ref_n is not None:
        #             print(import_ref_n)

        #         else:
        #             print("Key 'import_ref_n' not found in the 'data' object.")

        #     else:
        #         print("Key 'data' not found in the parsed JSON.")

        # else:
        #     print("The parsed JSON data is neither a dictionary nor a list.")

        # cont_num_response = invoke_http(IMPORT_CONT_URL + "/import_cont/cont_num/" + str(import_ref_n), method='GET')
        # cont_num_response = json.dumps(cont_num_response)
        # parsed_cont_num_response = json.loads(cont_num_response)
        # # cont_num = [container['container_num'] for container in parsed_cont_num_response['data']['container_nums']]
        # cont_num = None

        # if 'data' in parsed_cont_num_response:
        #     container_nums = parsed_cont_num_response['data'].get('container_nums', [])

        #     if container_nums:
        #         cont_num = [container['container_num'] for container in container_nums]
        #         print(cont_num)

        #     else:
        #         print("Key 'container_nums' not found in the 'data' object.")

        # else:
        #     print("Key 'data' not found in the parsed JSON.")

    #     if import_ref_n:
    #         return jsonify(
    #             {
    #                 "code":200,
    #                 "data":
    #                 {
    #                     "container_num" : import_ref_n

    #                 }
    #             }
    #         ),200

    # except Exception as e:
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "message": "Failed to retrieve container number because: " + str(e)
    #         }
    #     ), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8089, debug=True)