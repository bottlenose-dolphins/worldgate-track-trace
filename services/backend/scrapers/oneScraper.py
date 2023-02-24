from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return("hello")

@app.route('/ONE', methods=['POST'])

def oneScraper(tracking_type,identifier):

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

        data = request.get_json()

        tracking_type = data["tracking_type"]

        identifier = data["identifier"]

        # remove ONEY prefix from BL Number

        if tracking_type == "BL":

            identifier = identifier[4:]
        
        # Can interchange identifier with Container/BL Number as the process is similar

        driver.get('https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking?ctrack-field=' + identifier + '&trakNoParam=' + identifier)

        time.sleep(3)

        # Inline Frame present so need to change to this so you can extract values

        driver.switch_to.frame("IframeCurrentEcom")

        status = driver.find_element(By.XPATH, '//*[@id="1"]/td[9]').text

        #clicking the Container Number will show us more details like Port of Destination and ETA

        driver.find_element(By.XPATH, '//*[@id="1"]/td[4]/a').click()

        time.sleep(3)

        expectedArrivalTime = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[5]').text

        destinationPort = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[4]').text

        vesselName = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[1]').text

        if status != None:

            time.sleep(3)

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

        return jsonify(

            {

                "code": 500,

                "message": str(e)

            }

        ), 500

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8083, debug=True) #to work as a local flask app


# TESTING URL

# http://192.168.1.118:8084/ONE/BL/ONEYSINC72210300
# http://192.168.1.118:8084/ONE/BL/ONEYSINC69412601
# http://192.168.1.118:8084/ONE/CTR/GAOU6627318
# http://192.168.1.118:8084/ONE/CTR/TCNU7130634

