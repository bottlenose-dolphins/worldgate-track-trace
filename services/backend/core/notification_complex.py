from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http, invoke_http2
from os import getenv
from dotenv import load_dotenv
import json
import os
from twilio.rest import Client

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

@app.route("/addsubscription", methods=['POST'])
def addsubscription():
     if request.is_json:
        try:
            data = request.get_json()
            user_id = data["userid"]
            containerid=data["containerid"]
            status=data["status"]

            jsondata={
                "userid":user_id,
                "containerid":containerid,
                "status":status
            }
            response = invoke_http2("core_subscription", "subscription/add",prod, method='POST', json=jsondata)
            print(response)
        except Exception as e:
            return jsonify(
            {
                "code": 500,
                "message": e
            }
        ), 500
    
        return response

@app.route("/deletesubscription", methods=['POST'])
def deletesubscription():
     if request.is_json:
        try:
            data = request.get_json()
            containerid=data["containerid"]
            jsondata={
     
                "containerid":containerid
             
            }
            response = invoke_http2("core_subscription", "subscription/delete",prod, method='POST', json=jsondata)
            print(response)
        except Exception as e:
            return jsonify(
            {
                "code": 500,
                "message": e
            }
        ), 500
    
        return response
@app.route("/sendsms", methods=['POST'])
def sendsms():
    response = invoke_http2("core_subscription", "subscription/getsubscriptions",prod, method='POST')
    for i in range(len(response)):
        container=response[i]["container_id"]
        userid=response[i]["wguser_id"]
        subscription_status=response[i]["status"]
        shipment_type="ctr"
        directions="import"
        data={
            "identifier":container,
            "identifier_type":shipment_type,
            "direction":directions

        }
        identifier = container
        identifier_type = shipment_type
        direction = directions

            # print("\nReceived details in JSON:", data)

        if direction == "export":
            origin = "SINGAPORE"

        # Retrieve Master BL from House BL
        if identifier_type == "bl":
            if direction == "import":
                master_bl, origin, import_ref_n = get_import_master_bl(identifier)
            elif direction == "export":
                master_bl, export_ref_n = get_export_master_bl(identifier)            

            data = {
                        "identifier": master_bl,
                        "identifier_type": "bl"
                    }
        
        if identifier_type == "ctr":
            if direction == "import":
                master_bl, origin, import_ref_n = get_import_master_bl_ctr(identifier)
            elif direction == "export":
                master_bl, export_ref_n = get_export_master_bl_ctr(identifier)   
        
        # Retrieve shipping line's prefix
        prefix, vendor_name = get_prefix(master_bl, direction)

        # Invoke scraper microservice
        # shipment_info = invoke_http(scraper_url + prefix, method='POST', json=data)
        shipment_info = invoke_http2("scraper_"+ prefix, prefix, prod, method="POST", json=data)
        status=""
        if shipment_info:
        
            status = shipment_info["data"]["status"]

            # Update DB with latest shipment information
            

        response2=status
        
        if(subscription_status!=response2):
            updatedata={
                "containerid":identifier,
                "status":response2
            }
            
            useriddata={
            "wguserid":userid
            }
            phone_number=invoke_http2("core_user", "user/getnumber",prod, method='POST', json=useriddata)
            
            account_sid = "AC7a7b489784baef97d21697b086b468ec"
            auth_token = "eed37e9b4744d26ed34a67d4d3efe232"
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body="There has been a status update in regards to your Container Number: "+identifier+" Status:"+response2,
                from_="+15674004435",
                to = "+65"+str(phone_number)
                )
            update = invoke_http2("core_subscription", "subscription/update",prod, method='POST',json=updatedata)
        

    return jsonify({
                "code": 200,
                "message": "success"
            }),200

def get_prefix(master_bl, direction):
    data = {
            "master_bl": master_bl
        }

    # Invoke import_shipment/export_shipment microservice to retrieve cr_agent_id
    if direction == "import":
        # import_ref_res = invoke_http(import_shipment_url + "import_shipment/agent_id", method='POST', json=data)
        import_ref_res = invoke_http2("core_import_shipment", "import_shipment/agent_id", prod, method='POST', json=data)
        if import_ref_res["code"] == 200:
            data = {
                "vendor_id": import_ref_res["data"]["cr_agent_id"]
            } 
    elif direction == "export":
        # export_ref_res = invoke_http(export_shipment_url + "export_shipment/agent_id", method='POST', json=data)
        export_ref_res = invoke_http2("core_export_shipment", "export_shipment/agent_id", prod, method='POST', json=data)
        if export_ref_res["code"] == 200:
            data = {
                "vendor_id": export_ref_res["data"]["cr_agent_id"]
            } 

    # vendor_mast_res = invoke_http(vendor_mast_url + "vendor_mast/vendor_name", method='POST', json=data)        
    vendor_mast_res = invoke_http2("core_vendor_mast", "vendor_mast/vendor_name", prod, method="POST", json=data) 
    if vendor_mast_res["code"] == 200:
        data = {
            "vendor_name": vendor_mast_res["data"]["vendor_name"]
        }
        print(data)
        # prefix_res = invoke_http(prefix_url + "prefix/retrieve", method='POST', json=data)
        prefix_res = invoke_http2("core_prefix", "prefix/retrieve", prod, method='POST', json=data)
        if prefix_res["code"] == 200:
            prefix = prefix_res["data"]["prefix"]
            return prefix, vendor_mast_res["data"]["vendor_name"]

def get_import_master_bl(house_bl):
    # Invoke import microservice
    data = {
            "house_bl": house_bl
        }
    
    # response = invoke_http(import_url + "import/import_ref_n", method='POST', json=data)
    response = invoke_http2("core_import","import/import_ref_n", prod, method='POST', json=data)
    import_ref_n = response["data"]["import_ref_n"]

    # Invoke import_shipment microservice
    data = {
            "import_ref_n": import_ref_n
        }
    
    # response = invoke_http(import_shipment_url + "import_shipment/bl", method='POST', json=data)
    response = invoke_http2("core_import_shipment", "import_shipment/bl", prod, method='POST', json=data)
    master_bl = response["data"]["master_bl"]
    origin = response["data"]["origin"]
    
    return master_bl, origin, import_ref_n

# Retrieve Master B/L by House B/L (EXPORT)
def get_export_master_bl(house_bl):
    # Invoke export microservice
    data = {
            "house_bl": house_bl
        }
    
    # response = invoke_http(export_url + "export/export_ref_n", method='POST', json=data)
    response = invoke_http2("core_export","export/export_ref_n", prod, method='POST', json=data)
    export_ref_n = response["data"]["export_ref_n"]

    # Invoke export_shipment microservice
    data = {
            "export_ref_n": export_ref_n
        }
    
    # response = invoke_http(export_shipment_url + "export_shipment/bl", method='POST', json=data)
    response = invoke_http2("core_export_shipment", "export_shipment/bl", prod, method='POST', json=data)
    master_bl = response["data"]["master_bl"]

    return master_bl, export_ref_n
    
# Retrieve Master B/L by Container Number (IMPORT)
def get_import_master_bl_ctr(container_number):
    data = {
        "container_number": container_number
    }
    
    # import_cont_res = invoke_http(import_cont_url + "import_cont/import_ref_n", method='POST', json=data)
    import_cont_res = invoke_http2("core_import_cont", "import_cont/import_ref_n", prod, method='POST', json=data)
    import_ref_n = import_cont_res["data"]["import_ref_n"]
    data = {
        "import_ref_n": import_ref_n
    }
    
    # import_ref_res = invoke_http(import_shipment_url + "import_shipment/bl", method='POST', json=data)
    import_ref_res = invoke_http2("core_import_shipment", "import_shipment/bl", prod, method='POST', json=data)
    master_bl = import_ref_res["data"]["master_bl"]
    origin = import_ref_res["data"]["origin"]

    return master_bl, origin, import_ref_n

# Retrieve Master B/L by Container Number (EXPORT)
def get_export_master_bl_ctr(container_number):
    data = {
        "container_number": container_number
    }

    # export_cont_res = invoke_http(export_cont_url + "export_cont/export_ref_n", method='POST', json=data)
    export_cont_res = invoke_http2("core_export_cont", "export_cont/export_ref_n", prod, method='POST', json=data)
    export_ref_n = export_cont_res["data"]["export_ref_n"]

    data = {
        "export_ref_n": export_ref_n
    }
    
    # export_ref_res = invoke_http(export_shipment_url + "export_shipment/bl", method='POST', json=data)
    export_ref_res = invoke_http2("core_export_shipment", "export_shipment/bl", prod, method='POST', json=data)
    master_bl = export_ref_res["data"]["master_bl"]

    return master_bl, export_ref_n



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015, debug=True)