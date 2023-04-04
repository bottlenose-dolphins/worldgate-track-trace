from flask import Flask, jsonify, send_file, request
import boto3

app = Flask(__name__)

s3 = boto3.client('s3')

bucket = 'worldgate-tracktrace-docs'

@app.route('/bl_doc/download', methods=['POST'])
def download_bl_doc():
    try:
        # if container, retrieve HBL from container number

        # else, just use HBL
        data = request.get_json()
        hbl = data["hbl"] + ".pdf"
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
        hbl = data["hbl"] + ".pdf"
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
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014, debug=True)