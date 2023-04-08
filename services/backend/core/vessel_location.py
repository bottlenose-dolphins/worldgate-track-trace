#flask app
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

#making other api calls
from invokes import invoke_http, invoke_http2
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

#env related
from os import getenv
from dotenv import load_dotenv

#utils 
import json
from urllib.parse import quote
import re

load_dotenv()

app = Flask(__name__)
prod = getenv('prod', "0")
VESSEL_API_KEY = getenv('VESSEL_API_KEY', None)
LOCATION_API_KEY = getenv('LOCATION_API_KEY', None)

CORS(app, resources={r"/*": {"origins": "*"}}, origins="http://localhost:3000",
    supports_credentials=True, expose_headers="Set-Cookie")

print("prod type: ", type(prod))

@app.route("/ping", methods=['GET'])
def health_check():
    return("vessel location")

@app.route('/info', methods=['POST'])
def info():
    if request.is_json:

        # ONLY for testing purposes, so as not to use API PROVIDER CALLS
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "cords": [27.20849, 121.747275],
                        "destination_cords": [29.9360665448397, 121.844334447703]
                    }
                }
        ), 200
        data = request.get_json()
        print("\nReceived details in JSON:", data)

        vessel_name = data["vessel_name"]
        port_of_discharge = data["port_of_discharge"]

        prepared_vessel_name = prepare_vessel_name(vessel_name)
        try:
            imo = get_vessel_imo(prepared_vessel_name, VESSEL_API_KEY)
            print("*** Obtained IMO " + str(imo))
        
        except:
            #to create dictionary as backup later 

            #failure response
            print("*** Failed to get IMO")
            return jsonify(
                    {
                        "code": 500,
                        "message": "Unable to obtain Vessel IMO"
                    } 
                ), 500
        
        # try: 
        #     # sea routes api, low rate limit
        #     cords, destination_cords = get_vessel_location(imo, VESSEL_API_KEY)
        #     print("*** Using API provider: SEA ROUTES")

        # except:
        print("*** Using API provider: ZYLA")
        #zyla api, seems to be okay but takes way longer
        cords = get_vessel_location2(imo, LOCATION_API_KEY)
        destination_cords = []

        #logging
        print( "*** cords returned :")
        print(cords)
        print( "*** dest cords returned :")
        print(destination_cords)
            
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "cords": cords,
                        "destination_cords": destination_cords
                    }
                }
        ), 200
    

def prepare_vessel_name(vessel_name):
    """ 
    convert: 
    
        Gfs Giselle/Sgis-2301E --> Gfs Giselle
        Hyundai Supreme/0125N --> Hyundai Supreme
        Apollon D/Poll-02303E ---> Apollon D
        HMM ROTTERDAM 009E (OROT) -->  HMM ROTTERDAM
        

    no issue:
        YM CERTAINTY
    """
    prepared_vessel_name_list = []
    fragments = re.split(r'[\/\s]+', vessel_name)
    for fragment in fragments:
        if fragment.isalpha():
            prepared_vessel_name_list.append(fragment)
    #create new query and encode for url         
    return quote(" ".join(prepared_vessel_name_list), safe="")


def get_vessel_imo(vessel_name, API_KEY):
    """
    Tested with:

    strings = [
        "YM CONSTANCY",
        # "Gfs Giselle/Sgis-2301E",
        # "Hyundai Supreme/0125N",
        # "Apollon D/Poll-02303E",
        # "HMM ROTTERDAM 009E (OROT)",
        # "YM CERTAINTY",
        # "ONE TRIBUTE 020W (TIRT)"
    ]

    cannot_find = [
        # "Pelican/0014N" --> Pelican does not work
    ]
    """

    url = f"https://api.searoutes.com/vessel/v2/{vessel_name}/info"
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY
    }
    response_payload = invoke_http(url, method="GET", headers=headers)
    print("imo payload value:")
    print(type(response_payload[0]))
    print(response_payload[0])
    return response_payload[0]["imo"]


#sea routes which has a low rate limit (no longer used for now)
def get_vessel_location(imo, API_KEY):

    url = f"https://api.searoutes.com/vessel/v2/{imo}/eta"
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY
    }
    response_payload = invoke_http(url, method="GET", headers=headers)
    print("location payload value:")
    print(type(response_payload))
    print(response_payload)
    print(response_payload["position"])
    current_position =  response_payload["position"]["geometry"]["coordinates"][::-1]
    print("*** current position ***" )
    print(current_position)
    print(type(current_position[0]))
    print(type(current_position[1]))
    destination_position = response_payload["to"]["location"]["geometry"]["coordinates"][::-1]
    return [current_position, destination_position]

#long waiting time zyla api
def get_vessel_location2(imo, API_KEY):
    # url = f"https://api.searoutes.com/vessel/v2/{imo}/eta"
    url = f"https://zylalabs.com/api/78/vessel+traffic+information+api/1576/get+position?imoCode={imo}"
    headers = {
        "accept": "application/json",
        'Authorization': f'Bearer {API_KEY}'
    }
    response_payload = invoke_http(url, method="GET", headers=headers)
    return(string_to_cords(response_payload['data']['latitude_longitude']))

#for zyla api
def string_to_cords(coord_string):
    coord_list = coord_string.split("° / ")
    return [float(coord_list[0].strip()), float(coord_list[1].strip().rstrip("°"))]