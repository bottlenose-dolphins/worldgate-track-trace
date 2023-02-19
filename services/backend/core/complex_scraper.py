from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

scraper_url = "http://scraper_ymlu:8080/"
prefix_url = "http://core_prefix:5011/"
import_shipment_url = "http://core_import_shipment:5005/"
export_shipment_url = "http://core_export_shipment:5008/"
import_url = "http://core_import:5003/"
export_url = "http://core_export:5006/"
import_cont_url = "http://core_import_cont:5004/"
export_cont_url = "http://core_export_cont:5007/"

@app.route('/scrape', methods=['POST'])
def scrape():
    if request.is_json:
        try:
            data = request.get_json()
            shipping_line = data["shipping_line"]
            identifier = data["identifier"]
            identifier_type = data["identifier_type"]
            direction = data["direction"]
            prefix = data["identifier"][:4].lower()

            print("\nReceived details in JSON:", data)
            # {
            #    "shipping_line": "Yang Ming",
            #    "identifier": "YMLU3434431", <this will be House BL>
            #    "identifier_type": "ctr",
            #    "direction": "import"
            # }  

            # {
            #     "shipping_line": "Yang Ming",
            #     "identifier": "CTG-6463",
            #     "identifier_type": "bl",
            #     "direction": "export"
            # }
            # returns QCOU 502267

            # {
            #     "shipping_line": "Yang Ming",
            #     "identifier": "PKGSIN164134",
            #     "identifier_type": "bl",
            #     "direction": "import"
            # }
            # returns CBKKSIN04450

            # Retrieve Master BL from House BL
            if identifier_type == "bl":
                print("***going here?***")
                if direction == "import":
                    master_bl = get_import_master_bl(identifier)
                elif direction == "export":
                    master_bl = get_export_master_bl(identifier)            
                # Retrieve shipping line's prefix
                prefix = master_bl[:4].lower()
                data = {
                            "identifier": master_bl,
                            "identifier_type": "bl"
                        }
            
            prefix = "ymlu"

            # Invoke scraper microservice
            print("***invoking shipment_info***")
            shipment_info = invoke_http(scraper_url + prefix, method='POST', json=data)
            print(shipment_info)
            
            if shipment_info:
                arrival_date = shipment_info["data"]["arrival_date"]
                port_of_discharge = shipment_info["data"]["port_of_discharge"]
                vessel_name = shipment_info["data"]["vessel_name"]

                print(arrival_date)
                print(port_of_discharge)
                print(vessel_name)

                # Update DB with latest shipment information
                if identifier_type == "bl":
                    update_shipment_info_bl(master_bl, arrival_date, port_of_discharge, vessel_name, direction)
                elif identifier_type == "ctr":
                    update_shipment_info_cont(identifier, arrival_date, port_of_discharge, vessel_name, direction)
                
                return jsonify(shipment_info), 200

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
def check_prefix(shipping_line):
    data = {
            "shipping_line": shipping_line
        }
    
    response = invoke_http(prefix_url + "prefix/retrieve", method='POST', json=data)
    if response["data"]["code"] == 200:
        prefix = response["data"]["prefix"]
        return prefix

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
        response = invoke_http(import_shipment_url + "import_shipment/update", method='POST', json=data)
    elif direction == "export":
        response = invoke_http(export_shipment_url + "export_shipment/update", method='POST', json=data)
    return response

# Update F2K with latest shipment information (CONTAINER)
def update_shipment_info_cont(container_number, arrival_date, port_of_discharge, vessel_name, direction):
    data = {
        "container_number": container_number
    }

    # Select import or export
    if direction == "import":
        # Invoke import_ref microservice
        response = invoke_http(import_cont_url + "import_cont/import_ref_n", method='POST', json=data)
        import_ref_n = response["data"]["import_ref_n"]

        data = {
            "import_ref_n": import_ref_n,
            "arrival_date": arrival_date,
            "port_of_discharge": port_of_discharge,
            "vessel_name": vessel_name
        }

        # Invoke import_ref microservice
        response = invoke_http(import_shipment_url + "import_shipment/update_cont", method='POST', json=data)

    elif direction == "export":
        # Invoke export_cont microservice
        response = invoke_http(export_cont_url + "export_cont/export_ref_n", method='POST', json=data)
        export_ref_n = response["data"]["export_ref_n"]

        data = {
            "export_ref_n": export_ref_n,
            "arrival_date": arrival_date,
            "port_of_discharge": port_of_discharge,
            "vessel_name": vessel_name
        }

        # Invoke export_ref microservice
        response = invoke_http(export_shipment_url + "export_shipment/update_cont", method='POST', json=data)
        
    return response

# Retrieve Master B/L by House B/L (IMPORT)
def get_import_master_bl(house_bl):
    # Invoke import microservice
    data = {
            "house_bl": house_bl
        }
    
    response = invoke_http(import_url + "import/import_ref_n", method='POST', json=data)
    import_ref_n = response["data"]["import_ref_n"]

    # Invoke import_shipment microservice
    data = {
            "import_ref_n": import_ref_n
        }
    
    response = invoke_http(import_shipment_url + "import_shipment/bl", method='POST', json=data)
    master_bl = response["data"]["master_bl"]
    
    return master_bl

# Retrieve Master B/L by House B/L (EXPORT)
def get_export_master_bl(house_bl):
    # Invoke export microservice
    data = {
            "house_bl": house_bl
        }
    
    response = invoke_http(export_url + "export/export_ref_n", method='POST', json=data)
    export_ref_n = response["data"]["export_ref_n"]

    # Invoke export_shipment microservice
    data = {
            "export_ref_n": export_ref_n
        }
    
    response = invoke_http(export_shipment_url + "export_shipment/bl", method='POST', json=data)
    master_bl = response["data"]["master_bl"]
    
    return master_bl
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
    # app.run(host='0.0.0.0', debug=True)
    