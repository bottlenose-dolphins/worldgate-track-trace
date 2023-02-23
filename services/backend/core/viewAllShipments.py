from flask import Flask, jsonify, request
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http, invoke_http2
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

prod = getenv("prod")
print("prod type: ", type(prod))

print("********")

@app.route("/getExportContainerNum", methods=['POST'])
def getExportContainerNum():

    data = request.get_json()
    wguser_id = data['wguser_id']

    data = {
                "wguser_id" : wguser_id
            }

    # export_ref_num_response = invoke_http(EXPORT_URL + "/export/export_ref_n/wguser_id", method="POST", json=data)
    export_ref_num_response = invoke_http2("core_export", "export/export_ref_n/wguser_id", prod, method="POST", json=data)
    export_ref_num_dumped = json.dumps(export_ref_num_response)
    export_ref_num_loads = json.loads(export_ref_num_dumped)
    retrieved_output_from_export = export_ref_num_loads['data']['output']

    for a_record in retrieved_output_from_export:
        single_export_ref_num = a_record['export_ref_n']

        data = {
                    "export_ref_n" : single_export_ref_num
                }

        # container_num_response = invoke_http(EXPORT_CONT_URL + "/export_cont/container_num", method="POST", json=data)
        container_num_response = invoke_http2("core_export_cont", "export_cont/container_num", prod, method="POST", json=data)
        container_num_response_dumped = json.dumps(container_num_response)
        container_num_response_loads = json.loads(container_num_response_dumped)
        retrieved_list_containerNum_output = container_num_response_loads['data']['container_nums']

        if retrieved_list_containerNum_output:
            retrieved_tuple_containerNum_output = tuple(retrieved_list_containerNum_output)
            a_record["container_numbers"] = retrieved_tuple_containerNum_output
            a_record["type"] = "Export"

    return retrieved_output_from_export



@app.route("/getImportContainerNum", methods=['POST'])
def getImportContainerNum():

    data = request.get_json()
    wguser_id = data['wguser_id']

    data = {
                "wguser_id" : wguser_id
            }

    # import_ref_num_response = invoke_http(IMPORT_URL + "/import/import_ref_n/wguser_id", method="POST", json=data)
    import_ref_num_response = invoke_http2("core_import", "import/import_ref_n/wguser_id", prod, method="POST", json=data)
    import_ref_num_dumped = json.dumps(import_ref_num_response)
    import_ref_num_response_loads = json.loads(import_ref_num_dumped)
    retrieved_output_from_import = import_ref_num_response_loads['data']['output']

    for a_record in retrieved_output_from_import:
        single_import_ref_num = a_record['import_ref_n']

        data = {
                    "import_ref_n" : single_import_ref_num
                }

        # container_num_response = invoke_http(IMPORT_CONT_URL + "/import_cont/container_num", method="POST", json=data)
        container_num_response = invoke_http2("core_import_cont", "import_cont/container_num", prod, method="POST", json=data)
        container_num_response_dumped = json.dumps(container_num_response)
        container_num_response_loads = json.loads(container_num_response_dumped)
        retrieved_list_containerNum_output = container_num_response_loads['data']['container_nums']

        if retrieved_list_containerNum_output:
            retrieved_tuple_containerNum_output = tuple(retrieved_list_containerNum_output)
            a_record["container_numbers"] = retrieved_tuple_containerNum_output
            a_record["type"] = "Import"

    return retrieved_output_from_import

if __name__ == "__main__":

    # app.run(host='0.0.0.0', port=5010, debug=True)
    app.run(host='0.0.0.0', debug=True)


# ExportContainerNum API Endpoint

# http://127.0.0.1:5010/getExportContainerNum

# ExportContainerNum Sample JSON request

# {
#     "wguser_id" : "bk666dcoeZTH3dxZCuu4FR"
# }

# ExportContainerNum Sample JSON Response

# [
#     {
#         "arrival_date": "Thu, 22 Sep 2022 00:00:00 GMT",
#         "container_numbers": [
#             "APHU6142610",
#             "APHU6318274",
#             "APLU9023090",
#             "FSCU9928083",
#             "TCKU9278056"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21658,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "APHU6193752",
#             "APHU6240999",
#             "APHU6597013",
#             "APHU6638299",
#             "APHU6827522",
#             "GLDU7211691",
#             "TRLU5314819",
#             "TRLU5928484"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21699,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "NOSU2485582"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21693,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "CRXU9978904",
#             "FCIU8164504",
#             "GESU5550914",
#             "GLDU7458167",
#             "TOLU1522207",
#             "TRLU6634020",
#             "TRLU6841964"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21684,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "APHU6212488",
#             "APHU6240880",
#             "APHU6314833",
#             "APHU6548261",
#             "APHU6686337",
#             "APHU6687400",
#             "FCIU8417900"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21682,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "BSIU2133191",
#             "FCIU2261282",
#             "IPXU3757195",
#             "YMLU2880505",
#             "YMLU3018687",
#             "YMLU3085448"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21678,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "REGU4211519"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21673,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Tue, 15 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "TGHU0582887",
#             "WFHU1213294",
#             "YMLU2451516",
#             "YMLU2556950",
#             "YMLU3008652"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21677,
#         "type": "import"
#     },
#     {
#         "arrival_date": "Thu, 10 Jun 2004 00:00:00 GMT",
#         "container_numbers": [
#             "KMTU7319847"
#         ],
#         "import_destination": "Singapore",
#         "import_ref_n": 21696,
#         "type": "import"
#     }
# ]
