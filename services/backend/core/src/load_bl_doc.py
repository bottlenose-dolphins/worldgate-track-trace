from flask_cors import CORS
from flask import Flask, jsonify, send_file, request
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http, invoke_http2
from os import getenv
from dotenv import load_dotenv
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://www.worldgatetracktrace.click", "http://127.0.0.1", "http://worldgatetracktrace.click", "localhost"]}})

load_dotenv()
aws_access_key_id = getenv("aws_access_key_id")
aws_secret_access_key = getenv("aws_secret_access_key")
prod = getenv("prod")

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
bucket = 'worldgate-tracktrace-docs'


@app.route('/bl_doc/download', methods=['POST'])
def download_bl_doc():
    try:
        data = request.get_json()
        hbl = get_container_hbl(data)

        response = s3.get_object(Bucket=bucket, Key=hbl)
        return send_file(response['Body'], mimetype='application/pdf')
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Failed to retrieve hbl document: " + str(e)
            }
        ), 500

@app.route('/bl_doc/embed', methods=['POST'])
def embed_bl_doc():
    try:
        data = request.get_json()
        hbl = get_container_hbl(data)

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': hbl
            },
            ExpiresIn=3600
        )

        print(url)
        return url
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Failed to retrieve hbl url: " + str(e)
            }
        ), 500
    
def get_container_hbl(data):
    identifier = data["identifier"]
    identifier_type = data["identifier_type"]
    direction = data["direction"]

    if identifier_type == "ctr":
        if direction == "import":
            # find IMPORT_REF_N by CONT_N in IMPORT_REF_CONT
            data = {
                "container_number": identifier
            }
            import_cont_res = invoke_http2("core_import_cont", "import_cont/import_ref_n", prod, method='POST', json=data)
            import_ref_n = import_cont_res["data"]["import_ref_n"]

            # find HBL by IMPORT_REF_N in IMPORT
            data = {
                "import_ref_n": import_ref_n
            }
            import_res = invoke_http2("core_import","import/hbl", prod, method='POST', json=data)
            hbl = import_res["data"]["hbl"] + ".pdf"
        
        elif direction == "export":
            # find EXPORT_REF_N by CONT_N in EXPORT_REF_CONT
            data = {
                "container_number": identifier
            }
            export_cont_res = invoke_http2("core_export_cont", "export_cont/export_ref_n", prod, method='POST', json=data)
            export_ref_n = export_cont_res["data"]["export_ref_n"]

            # find HBL by EXPORT_REF_N in EXPORT
            data = {
                "export_ref_n": export_ref_n
            }
            export_res = invoke_http2("core_export","export/hbl", prod, method='POST', json=data)
            hbl = export_res["data"]["hbl"] + ".pdf"

    elif identifier_type == "bl":
        hbl = identifier + ".pdf"
    
    return hbl

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014, debug=True)