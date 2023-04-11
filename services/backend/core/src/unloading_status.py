from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http, invoke_http2
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, origins="http://localhost:3000",
     supports_credentials=True, expose_headers="Set-Cookie")

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(getenv('SQLALCHEMY_DATABASE_URI'))

prod = getenv("prod")
print("prod type: ", type(prod))

print("********")

db = SQLAlchemy(app)

@app.route('/unloading_status', methods=['POST'])
def get_unloading_status():
    try:
        data = request.get_json()
        identifier = data["identifier"]
        identifier_type = data["identifier_type"]
        direction = data["direction"]

        # Retrieve Master BL from House BL
        if identifier_type == "bl":
            if direction == "import":
                master_bl = get_import_master_bl(identifier)
            elif direction == "export":
                master_bl = get_export_master_bl(identifier)            
        
        if identifier_type == "ctr":
            if direction == "import":
                master_bl = get_import_master_bl_ctr(identifier)
            elif direction == "export":
                master_bl = get_export_master_bl_ctr(identifier)   

        # Get Shipment's Job Type (FCL or LCL), Container Release Status and Delivery Taken status
        response = get_cont_status(master_bl, direction)
        
        if response["job_type"] == "F":
            return jsonify(
                    {
                    "code": 200,
                    "data": {
                            "master_bl": response["master_bl"],
                            "cont_released": response["cont_released"],
                            "del_taken": response["del_taken"]
                        }
                    }
                ), 200
        else:
            return jsonify(
                {
                    "code": 200,
                    "message": "Shipment's job type is not FCL"
                }
            )
    
    except:
        return jsonify(
            {
                "code": 200,
                "message": "Failed to retrieve shipment's unloading status"
            }
        )
    

# Get Shipment's Job Type (FCL or LCL), Container Release Status and Delivery Taken status based on Master B/L
def get_cont_status(master_bl, direction):
    data = {
        "master_bl": master_bl
    }
    
    if direction == "import":
        res = invoke_http2("core_import_shipment", "import_shipment/cont_status", prod, method='POST', json=data)
        return res["data"]
    
    elif direction == "export":
        res = invoke_http2("core_export_shipment", "export_shipment/cont_status", prod, method='POST', json=data)
        return res["data"]
    
# Retrieve Master B/L by House B/L (IMPORT)
def get_import_master_bl(house_bl):
    # Invoke import microservice
    data = {
            "house_bl": house_bl
        }
    
    response = invoke_http2("core_import","import/import_ref_n", prod, method='POST', json=data)
    import_ref_n = response["data"]["import_ref_n"]

    # Invoke import_shipment microservice
    data = {
            "import_ref_n": import_ref_n
        }
    
    response = invoke_http2("core_import_shipment", "import_shipment/bl", prod, method='POST', json=data)
    master_bl = response["data"]["master_bl"]
    
    return master_bl

# Retrieve Master B/L by House B/L (EXPORT)
def get_export_master_bl(house_bl):
    # Invoke export microservice
    data = {
            "house_bl": house_bl
        }
    
    response = invoke_http2("core_export","export/export_ref_n", prod, method='POST', json=data)
    export_ref_n = response["data"]["export_ref_n"]

    # Invoke export_shipment microservice
    data = {
            "export_ref_n": export_ref_n
        }
    
    response = invoke_http2("core_export_shipment", "export_shipment/bl", prod, method='POST', json=data)
    master_bl = response["data"]["master_bl"]

    return master_bl
    
# Retrieve Master B/L by Container Number (IMPORT)
def get_import_master_bl_ctr(container_number):
    data = {
        "container_number": container_number
    }
    
    import_cont_res = invoke_http2("core_import_cont", "import_cont/import_ref_n", prod, method='POST', json=data)
    import_ref_n = import_cont_res["data"]["import_ref_n"]
    data = {
        "import_ref_n": import_ref_n
    }
    
    import_ref_res = invoke_http2("core_import_shipment", "import_shipment/bl", prod, method='POST', json=data)
    master_bl = import_ref_res["data"]["master_bl"]

    return master_bl

# Retrieve Master B/L by Container Number (EXPORT)
def get_export_master_bl_ctr(container_number):
    data = {
        "container_number": container_number
    }

    export_cont_res = invoke_http2("core_export_cont", "export_cont/export_ref_n", prod, method='POST', json=data)
    export_ref_n = export_cont_res["data"]["export_ref_n"]

    data = {
        "export_ref_n": export_ref_n
    }
    
    export_ref_res = invoke_http2("core_export_shipment", "export_shipment/bl", prod, method='POST', json=data)
    master_bl = export_ref_res["data"]["master_bl"]

    return master_bl

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5013, debug=True)
    # app.run(host='0.0.0.0', debug=True)
