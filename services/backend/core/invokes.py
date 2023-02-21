import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from obtainIp import obtainIP

SUPPORTED_HTTP_METHODS = set([
    "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
])

DEV_IP = {
"scraper_ymlu" : "scraper_ymlu:8080",
"scraper_good": "scraper_good:8081",
"scraper_kmtc": "scraper_kmtc:8082",
"scraper_one": "scraper_one:8083",
"scraper_cord": "scraper_cord:8084",
"scraper_cosc": "scraper_cosc:8084",

"core_user" : "core_user:5002",
"core_import" : "core_import:5003",
"core_import_cont" : "core_import_cont:5004",
"core_import_shipment" : "core_import_shipment:5005",
"core_export" : "core_export:5006",
"core_export_cont" : "core_export_cont:5007",
"core_export_shipment" : "core_export_shipment:5008",
"core_complex_scraper" : "core_complex_scraper:5009",
"core_viewall" : "core_viewall:5010",
"core_prefix" : "core_prefix:5011",
"core_vendor_mast" : "core_vendor_mast:5012"
}


def invoke_http2(service, route, prod, method='GET', json=None, **kwargs):
    """A simple wrapper for requests methods.
       url: the url of the http service;
       method: the http method;
       data: the JSON input when needed by the http method;
       return: the JSON reply content from the http service if the call succeeds;
            otherwise, return a JSON object with a "code" name-value pair.
    """
    print("****just invoked invoke_http method in invokes.py")
    code = 200
    result = {}

    try:
        print("**** starting url resolution in invokes.py")
        if method.upper() in SUPPORTED_HTTP_METHODS:
            match prod:
                case True:
                    url = "http://" + obtainIP(service) + "/"
                case False:
                    url = "http://" + DEV_IP[service] + "/"
                case _:
                    url = None
                    raise Exception("Prod type was not specified")
                
            print("**** about to make request from invokes.py ****")
            r = requests.request(method, url+route, json = json, **kwargs)
            # r = requests.post(url, json=json, **kwargs)
            print("**** requests runs ****")
        else:
            raise Exception("HTTP method {} unsupported.".format(method))
    except Exception as e:
        code = 500
        if url == None:
            result = {"code": code, "message": "URL was not resolved by invokes module" + str(e)}         
        else:
            result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
    if code not in range(200,300):
        return result

    ## Check http call result
    if r.status_code != requests.codes.ok:
        code = r.status_code
    try:
        result = r.json() if len(r.content)>0 else ""
    except Exception as e:
        code = 500
        result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}

    return result



def invoke_http(url, method='GET', json=None, **kwargs):
    """A simple wrapper for requests methods.
       url: the url of the http service;
       method: the http method;
       data: the JSON input when needed by the http method;
       return: the JSON reply content from the http service if the call succeeds;
            otherwise, return a JSON object with a "code" name-value pair.
    """
    print("****just invoked invoke_http in invokes.py")
    code = 200
    result = {}

    try:
        if method.upper() in SUPPORTED_HTTP_METHODS:
            print("**** about to make request from invokes.py ****")
            r = requests.request(method, url, json = json, **kwargs)
            # r = requests.post(url, json=json, **kwargs)
            print("**** requests runs ****")
        else:
            raise Exception("HTTP method {} unsupported.".format(method))
    except Exception as e:
        code = 500
        result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
    if code not in range(200,300):
        return result

    ## Check http call result
    if r.status_code != requests.codes.ok:
        code = r.status_code
    try:
        result = r.json() if len(r.content)>0 else ""
    except Exception as e:
        code = 500
        result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}

    return result

