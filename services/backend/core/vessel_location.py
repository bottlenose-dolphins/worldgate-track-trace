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

#sea routes api key
VESSEL_API_KEY = getenv('VESSEL_API_KEY', None)

#zyla api key
LOCATION_API_KEY = getenv('LOCATION_API_KEY', None)

#gmaps api key
GMAPS_API_KEY = getenv('GMAPS_API_KEY', None)

CORS(app, resources={r"/*": {"origins": "*"}}, origins="http://localhost:3000",
    supports_credentials=True, expose_headers="Set-Cookie")

print("prod type: ", type(prod))

@app.route("/ping", methods=['GET'])
def health_check():
    return("vessel location")

# main method
@app.route('/info', methods=['POST'])
def info():
    if request.is_json:

    # ONLY for testing purposes, so as not to use API PROVIDER CALLS
    # ***************************************************************
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "cords": [27.20849, 121.747275],
                        "destination_cords": [29.9360665448397, 121.844334447703]
                    }
                }
        ), 200
    # ***************************************************************
        data = request.get_json()
        print("\nReceived details in JSON:", data)

        vessel_name = data["vessel_name"]
        port_of_discharge = data["port_of_discharge"]

        prepared_vessel_name = prepare_vessel_name(vessel_name)
        try:
            imo = get_vessel_imo(prepared_vessel_name, VESSEL_API_KEY)
            print("*** Obtained IMO " + str(imo))
        
        except:
            #may create a dictionary of names to imo mapping in case of failures
            #failure response
            print("*** Failed to get IMO")
            return jsonify(
                    {
                        "code": 500,
                        "message": "Unable to obtain Vessel IMO"
                    } 
                ), 500
        
        #we try to use sea routes api first in try, if we cant, then except will use zyla api
        try: 
            # sea routes api, low rate limit
            cords, destination_cords = get_vessel_location(imo, VESSEL_API_KEY)
            print("*** Using API provider: SEA ROUTES")

        except:
            print("*** Using API provider: ZYLA")
            #if sea routes api fails, use zyla api, seems to be okay but takes way longer and does not return destination coords
            cords = get_vessel_location2(imo, LOCATION_API_KEY)
            destination_cords = []

        #logging
        print( "*** cords returned :")
        print(cords)
        print( "*** dest cords returned :")
        print(destination_cords)

        #guarantee return of coords unless GMAPS cant find coords
        try: 
            if len(destination_cords)==0:
                print( "*** attempting to retrieve coords from gmaps")
                destination_cords = get_destination_coords_from_port_name_string(port_of_discharge, GMAPS_API_KEY)
                print( "*** successfully retrieved coords from gmaps")
        except:
            print( "*** failed to retrieve coords from gmaps")
            pass
            
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "cords": cords,
                        "destination_cords": destination_cords
                    }
                }
        ), 200
    
# ************* helper methods *************
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
    #to prevent Pelican from failing, return imo
    if vessel_name == "Pelican":
        return 9626560 

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


#sea routes which has a low rate limit
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

#long waiting time zyla api, this additionally uses the method 'string to cords' below, this is done so as to convert the response from zyla to smth similar to sea route's api
def get_vessel_location2(imo, API_KEY):
    # url = f"https://api.searoutes.com/vessel/v2/{imo}/eta"
    url = f"https://zylalabs.com/api/78/vessel+traffic+information+api/1576/get+position?imoCode={imo}"
    headers = {
        "accept": "application/json",
        'Authorization': f'Bearer {API_KEY}'
    }
    response_payload = invoke_http(url, method="GET", headers=headers)
    return(string_to_cords(response_payload['data']['latitude_longitude']))

#for zyla api response formatting, this is used in get_vessel_location2
def string_to_cords(coord_string):
    coord_list = coord_string.split("° / ")
    return [float(coord_list[0].strip()), float(coord_list[1].strip().rstrip("°"))]

#using a gmap search to get coords for destination

def get_destination_coords_from_port_name_string(port_name, API_KEY):
    safe_port_name = quote(port_name, safe="")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={safe_port_name}&key={API_KEY}"
    response_payload = invoke_http(url, method="GET")
    lat = response_payload["results"][0]["geometry"]["location"]["lat"]
    lng = response_payload["results"][0]["geometry"]["location"]["lng"]
    return[lat, lng]