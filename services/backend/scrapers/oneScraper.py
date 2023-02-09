from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from flask import Flask, jsonify, request, redirect, url_for

app = Flask(__name__)

# @app.route('/ONE/<string:tracking_type>/<string:identifier>')
@app.route("/ONE", methods=['POST'])

def oneScraper():

    # JSON Sample Request

    # {

    #     "tracking_type": "BL",

    #     "identifier": "ONEYSINC72210300"

    # }

    try:

        # headless mode will run the webscraping in the background and lesser RAM will be utilised --> Much more efficient process

        options = Options()

        # options.headless = True

        options.add_argument('--no-sandbox')

        options.add_argument('--headless')

        options.add_argument('--disable-gpu')

        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)

        driver.maximize_window()

        # remove ONEY prefix from BL Number

        data = request.get_json()

        tracking_type = data["tracking_type"]

        identifier = data["identifier"]

        if tracking_type == "BL":

            identifier = identifier[4:]
        
        # Can interchange identifier with Container/BL Number as the process is similar

        driver.get('https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking?ctrack-field=' + identifier + '&trakNoParam=' + identifier)

        time.sleep(7)

        # Inline Frame present so need to change to this so you can extract values

        driver.switch_to.frame("IframeCurrentEcom")

        status = driver.find_element(By.XPATH, '//*[@id="1"]/td[9]').text

        #clicking the Container Number will show us more details like Port of Destination and ETA

        driver.find_element(By.XPATH, '//*[@id="1"]/td[4]/a').click()

        time.sleep(7)

        expectedArrivalTime = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[5]').text

        destinationPort = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[4]').text

        vesselName = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[1]').text

        if status != None:

            time.sleep(7)

            return jsonify(

                {

                    "code": 200,

                    "data":{

                        "status": status,

                        "vessel_name": vesselName,

                        "port_of_discharge": destinationPort,

                        "time_of_arrival": expectedArrivalTime[8:]

                    }

                }

            )
        
        else:

            return jsonify(

                {

                    "code": 200,

                    "data":{

                        "message" : "No Status Found"

                    }

                }

            )

    except Exception as e:

        if e == "Message: no such element: Unable to locate element: {\"method\":\"xpath\",\"selector\":\"//*[@id=\"1\"]/td[9]\"}\n  (Session info: headless chrome=109.0.5414.74)\nStacktrace:\n#0 0xaaaacbf06bc4 <unknown>\n#1 0xaaaacbccd438 <unknown>\n#2 0xaaaacbd03924 <unknown>\n#3 0xaaaacbd36fcc <unknown>\n#4 0xaaaacbcf85dc <unknown>\n#5 0xaaaacbcf9ad4 <unknown>\n#6 0xaaaacbf893cc <unknown>\n#7 0xaaaacbf40d44 <unknown>\n#8 0xaaaacbf4087c <unknown>\n#9 0xaaaacbf851f0 <unknown>\n#10 0xaaaacbf4170c <unknown>\n#11 0xaaaacbf25800 <unknown>\n#12 0xaaaacbf4ca14 <unknown>\n#13 0xaaaacbf4cba0 <unknown>\n#14 0xaaaacbf631cc <unknown>\n#15 0xffff8bf2b648 start_thread\n#16 0xffff8b981c1c <unknown>\n" :

            return redirect("oneScraper")

        else:

            return jsonify(

            {

                "code": 500,

                "message": str(e)

            }

        ), 500



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8083, debug=True)


# TESTING URL

# http://192.168.1.118:8083/ONE/BL/ONEYSINC72210300
# http://192.168.1.118:8083/ONE/BL/ONEYSINC69412601
# http://192.168.1.118:8083/ONE/CTR/GAOU6627318
# http://192.168.1.118:8083/ONE/CTR/TCNU7130634

