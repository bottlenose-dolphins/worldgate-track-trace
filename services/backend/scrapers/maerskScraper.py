from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return("hello")

@app.route('/maersk', methods=['POST']) 

def oneScraper():

    try:
        data = request.get_json()
        identifier_type = data["identifier_type"]
        identifier = data["identifier"]
        
        options = Options()
        # options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        driver.get("https://www.maersk.com/tracking/" + identifier)
        time.sleep(10)
        
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/button[3]').click()
        time.sleep(5)
        # /html/body/div[1]/div/div/div[1]/div[2]/button[3]

        startingDestination = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/dl/dd[2]').text
        finalDestination = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/dl/dd[3]').text
        eta = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[2]/dl/dd[1]').text
        lastLocationAndStatus = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[2]/dl/dd[2]').text

        time.sleep(10)
        

        if lastLocationAndStatus != None:
            # time.sleep(10)
            return jsonify(
                {
                    "code": 200,
                    "data":{
                        "starting destination": startingDestination,
                        "finalDestination": finalDestination,
                        "arrival_date_and_time": eta,
                        "last_location_and_status": lastLocationAndStatus
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
    
    driver.quit()

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8086, debug=True)
    app.run(debug=True)
