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

@app.route('/sinokor', methods=['POST']) 

def sinokorScraper():

    try:

        data = request.get_json()
        identifier_type = data["identifier_type"]
        identifier = data["identifier"]
        
        options = Options()
        # options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920,1080")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        driver.get("http://ebiz.sinokor.co.kr/?lang=EN")
        time.sleep(3)

        search_box = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/div[2]/div/div[2]/div/input')
        search_box.send_keys(identifier)
        time.sleep(3)

        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[2]/button').click()
        time.sleep(5)

        if identifier_type == "ctr":
            time.sleep(5)
            driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div/div[2]/div/table/tbody/tr/td[1]/a').click()
            time.sleep(5)
        
        vessel_name = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/div/div[1]/div/ul/li[1]/b/a').text
        starting_destination_and_departure_timedate = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/div/div[1]/div/ul/li[2]/div[1]').text
        # departure_timeDate = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/div/div[1]/div/ul/li[2]/div[1]/span[2]').text
        final_destination_and_eta_timedate = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/div/div[1]/div/ul/li[2]/div[2]').text
        # eta_timeDate = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[2]/div/div[1]/div/ul/li[2]/div[2]/span[2]').text
        time.sleep(5)

        startingDestList = []

        for a_line in starting_destination_and_departure_timedate.split("\n"):
            startingDestList.append(a_line)
        
        starting_destination = startingDestList[0]
        starting_port = startingDestList[1]
        departure_timedate = startingDestList[2]

        finalDestList = []

        for a_line in final_destination_and_eta_timedate.split("\n"):
            finalDestList.append(a_line)
        
        final_destination = finalDestList[0]
        destination_port = finalDestList[1]
        eta_timedate = finalDestList[2]

        if vessel_name != None:
            return jsonify(
                {
                    "code": 200,
                    "data":{
                        "vessel name" : vessel_name,
                        "starting destination" : starting_destination,
                        "starting port" : starting_port,
                        "time of departure" : departure_timedate,
                        "final destination" : final_destination,
                        "destination port" : destination_port,
                        "eta" : eta_timedate
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
    app.run(host='0.0.0.0', port=8087, debug=True)
    # app.run(debug=True)







