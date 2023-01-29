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

scraper_url = "http://localhost:8080/"
prefix_url = "http://localhost:8082/"
import_shipment_url = "http://localhost:8083/"
export_shipment_url = "http://localhost:8084/"
import_url = "http://localhost:8085/"
export_url = "http://localhost:8086/"

@app.route('/scrape', methods=['POST'])
def scrape():
    if request.is_json:
        try:
            data = request.get_json()
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
        
            # Retrieve shipping line's prefix
            # shipping_line = data["shipping_line"]
            # prefix = check_prefix(shipping_line)
            # prefix = "ymlu"

            # Retrieve Master BL from House BL
            direction = data["direction"]
            if data["identifier_type"] == "bl":
                if direction == "import":
                    master_bl = get_import_master_bl(data["identifier"])
                elif direction == "export":
                    master_bl = get_export_master_bl(data["identifier"])
                data = {
                            "identifier": master_bl,
                            "identifier_type": "bl"
                        }
                return master_bl
            
            # Invoke scraper microservice
            # shipment_info = invoke_http(scraper_url + prefix, method='POST', json=data)
            
            # arrival_date = shipment_info["data"]["arrival_date"]
            # port_of_discharge = shipment_info["data"]["port_of_discharge"]
            # vessel_name = shipment_info["data"]["vessel_name"]

            # Update DB with latest shipment information
            # update_shipment_info(master_bl, arrival_date, port_of_discharge, vessel_name, direction)
            
            # return jsonify(shipment_info), 200

        except Exception as e:
            return jsonify(
            {
                "code": 500,
                "message": str(e)
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

# Update F2K with latest shipment information
def update_shipment_info(master_bl, arrival_date, port_of_discharge, vessel_name, direction):
    data = {
            "master_bl": master_bl,
            "arrival_date": arrival_date,
            "port_of_discharge": port_of_discharge,
            "vessel_name": vessel_name
        }

    # Select import_shipment or export_shipment microservice based on port_of_discharge
    if direction == "import":
        response = invoke_http(import_shipment_url + "import_shipment/update", method='POST', json=data)
    elif direction == "export":
        response = invoke_http(export_shipment_url + "export_shipment/update", method='POST', json=data)
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
    
    response = invoke_http(import_url + "export/export_ref_n", method='POST', json=data)
    export_ref_n = response["data"]["export_ref_n"]

    # Invoke export_shipment microservice
    data = {
            "export_ref_n": export_ref_n
        }
    
    response = invoke_http(export_shipment_url + "export_shipment/bl", method='POST', json=data)
    master_bl = response["data"]["master_bl"]
    
    return master_bl
    
if __name__ == '__main__':
    app.run(port=8081, debug=True)
    