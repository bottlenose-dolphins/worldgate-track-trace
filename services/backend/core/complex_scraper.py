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

# scraper_url = "http://scraper_ymlu:8080/"
# prefix_url = "http://core_prefix:5011/"
# import_shipment_url = "http://core_import_shipment:5005/"
# export_shipment_url = "http://core_export_shipment:5008/"
# import_url = "http://core_import:5003/"
# export_url = "http://core_export:5006/"
# import_cont_url = "http://core_import_cont:5004/"
# export_cont_url = "http://core_export_cont:5007/"
# vendor_mast_url = "http://core_vendor_mast:5012/"

@app.route("/ping", methods=['GET'])
def health_check():
    return("complex_scraper")

@app.route('/scrape', methods=['POST'])
def scrape():
    if request.is_json:
        try:
            data = request.get_json()
            identifier = data["identifier"]
            identifier_type = data["identifier_type"]
            direction = data["direction"]

            print("\nReceived details in JSON:", data)

            if direction == "export":
                origin = "SINGAPORE"

            # Retrieve Master BL from House BL
            if identifier_type == "bl":
                if direction == "import":
                    master_bl, origin = get_import_master_bl(identifier)
                elif direction == "export":
                    master_bl = get_export_master_bl(identifier)            

                data = {
                            "identifier": master_bl,
                            "identifier_type": "bl"
                        }
            
            if identifier_type == "ctr":
                if direction == "import":
                    master_bl, origin = get_import_master_bl_ctr(identifier)
                elif direction == "export":
                    master_bl = get_export_master_bl_ctr(identifier)   
            
            # Retrieve shipping line's prefix
            prefix, vendor_name = get_prefix(master_bl, direction)

            # Invoke scraper microservice
            # shipment_info = invoke_http(scraper_url + prefix, method='POST', json=data)
            shipment_info = invoke_http2("scraper_"+ prefix, prefix, prod, method="POST", json=data)
            
            if shipment_info:
                arrival_date = shipment_info["data"]["arrival_date"]
                port_of_discharge = shipment_info["data"]["port_of_discharge"]
                vessel_name = shipment_info["data"]["vessel_name"]

                # Update DB with latest shipment information
                if identifier_type == "bl":
                    update_shipment_info_bl(master_bl, arrival_date, port_of_discharge, vessel_name, direction)
                elif identifier_type == "ctr":
                    update_shipment_info_cont(identifier, arrival_date, port_of_discharge, vessel_name, direction)
                
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                                "arrival_date": arrival_date,
                                "port_of_discharge": port_of_discharge,
                                "vessel_name": vessel_name,
                                "shipping_line": vendor_name,
                                "port_of_loading": origin
                            }
                    }
                ), 200

        except Exception as e:
            return jsonify(
            {
                "code": 500,
                "message": "Failed to scrape for shipment information because " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }
    ), 400

# Retrieve prefix for respective shipping line
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

# Update F2K with latest shipment information (BL)
def update_shipment_info_bl(master_bl, arrival_date, port_of_discharge, vessel_name, direction):
    data = {
            "master_bl": master_bl,
            "arrival_date": arrival_date,
            "port_of_discharge": port_of_discharge,
            "vessel_name": vessel_name
        }

    # Select import_shipment or export_shipment microservice
    if direction == "import":
        # response = invoke_http(import_shipment_url + "import_shipment/update", method='POST', json=data)
        response = invoke_http2("core_import_shipment", "import_shipment/update",prod, method='POST', json=data)
    elif direction == "export":
        # response = invoke_http(export_shipment_url + "export_shipment/update", method='POST', json=data)
        response = invoke_http2("core_export_shipment", "export_shipment/update", prod, method='POST', json=data)
    return response

# Update F2K with latest shipment information (CONTAINER)
def update_shipment_info_cont(container_number, arrival_date, port_of_discharge, vessel_name, direction):
    data = {
        "container_number": container_number
    }

    # Select import or export
    if direction == "import":
        # Invoke import_ref microservice
        # response = invoke_http(import_cont_url + "import_cont/import_ref_n", method='POST', json=data)
        response = invoke_http2("core_import_cont", "import_cont/import_ref_n", prod, method='POST', json=data)
        import_ref_n = response["data"]["import_ref_n"]

        data = {
            "import_ref_n": import_ref_n,
            "arrival_date": arrival_date,
            "port_of_discharge": port_of_discharge,
            "vessel_name": vessel_name
        }

        # Invoke import_ref microservice
        # response = invoke_http(import_shipment_url + "import_shipment/update_cont", method='POST', json=data)
        response = invoke_http2("core_import_shipment", "import_shipment/update_cont", prod, method='POST', json=data)

    elif direction == "export":
        # Invoke export_cont microservice
        # response = invoke_http(export_cont_url + "export_cont/export_ref_n", method='POST', json=data)
        response = invoke_http2("core_export_cont", "export_cont/export_ref_n", prod, method='POST', json=data)
        export_ref_n = response["data"]["export_ref_n"]

        data = {
            "export_ref_n": export_ref_n,
            "arrival_date": arrival_date,
            "port_of_discharge": port_of_discharge,
            "vessel_name": vessel_name
        }

        # Invoke export_ref microservice
        # response = invoke_http(export_shipment_url + "export_shipment/update_cont", method='POST', json=data)
        response = invoke_http2("core_export_shipment", "export_shipment/update_cont", prod, method='POST', json=data)
        
    return response

# Retrieve Master B/L by House B/L (IMPORT)
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
    
    return master_bl, origin

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
    
    return master_bl
    
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
    return master_bl, origin

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
    return master_bl

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
    # app.run(host='0.0.0.0', debug=True)
    