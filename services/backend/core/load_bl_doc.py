from flask import Flask, jsonify, send_file, request
import boto3

app = Flask(__name__)

s3 = boto3.client('s3')

@app.route('/download_s3_object', methods=['POST'])
def download_s3_object():
    try:
        # if container, retrieve HBL from container number

        # else, just use HBL
        data = request.get_json()
        hbl = data["hbl"] + ".pdf"
        response = s3.get_object(Bucket='worldgate-tracktrace-docs', Key=hbl)
        return send_file(response['Body'], mimetype='application/pdf')
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "Failed to retrieve hbl document: " + str(e)
            }
        ), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014, debug=True)