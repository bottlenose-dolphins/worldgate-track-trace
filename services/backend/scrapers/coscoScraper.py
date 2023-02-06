from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# prefix: COAU, COSU, CCLU
@app.route("/cosco", methods=["POST"])
def coscoScraper():
    try:
        data = request.get_json()
        identifier_type = data["identifier_type"]
        identifier = data["identifier"]
        if identifier_type == "bl":
            # truncate prefix
            identifier = identifier[4:]

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        driver.get("https://elines.coscoshipping.com/ebusiness/cargotracking")
        time.sleep(1)

        if identifier_type == "ctr": # because default is B/L
            driver.find_element(By.CLASS_NAME, 'ivu-select-single').click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//*[@class='ivu-select-item'][contains(text(),'Container')]").click()

        # enter ctr/bl number into input field
        driver.find_element(By.XPATH,"//*[@id='wrap']//*[@class='ivu-input']").send_keys(identifier)
        # click search button
        driver.find_element(By.CLASS_NAME, 'btnSearch').click()
        time.sleep(2)

        if identifier_type == "bl":
            arrival_datetime = driver.find_element(By.XPATH, "//*[@class='ivu-c-detailPart']/div[4]/div[4]/p").text.strip('"').strip()
            print("ARRIVAL DATETIME IS: " + arrival_datetime)
            vessel_name = driver.find_element(By.XPATH, "//*[@class='ivu-table-row']/td[1]/div[1]/a[1]").text
            print("VESSEL NAME IS: " + vessel_name)
            port_of_discharge = driver.find_element(By.XPATH, "//*[@class='ivu-c-detailPart']/div[3]/div[4]/p").text.strip('"').strip()
            print("PORT OF DISCHARGE IS: " + port_of_discharge)

            arrival_date = arrival_datetime.split()[0]

        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "arrival_date": arrival_date,
                        "port_of_discharge": port_of_discharge,
                        "vessel_name": vessel_name
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
    
    finally:
        driver.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8079, debug=True) # TODO: CHANGE PORT???