from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request
import time
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://worldgatetracktrace.click, http://127.0.0.1"}})

# CTR Test
# identifier = "OOLU4299134"
# identifier_type = "ctr"

# BL Test
# identifier = "COAU7242927890"
# identifier_type = "bl"

# prefix: COAU, COSU, PASU, CCLU, OOCL
@app.route("/cosc", methods=["POST"])
def coscoScraper():
    try:
        data = request.get_json()
        identifier_type = data["identifier_type"]
        identifier = data["identifier"]
        if identifier_type == "bl":
            # truncate prefix
            identifier = identifier[4:]

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
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

        arrival_datetime = None
        port_of_discharge = None
        vessel_name = None

        if identifier_type == "bl":
            arrival_datetime = driver.find_element(By.XPATH, "//*[@class='ivu-c-detailPart']/div[4]/div[4]/p").text.strip('"').strip()
            vessel_name = driver.find_element(By.XPATH, "//*[@class='ivu-table-row']/td[1]/div[1]/a[1]").text
            port_of_discharge = driver.find_element(By.XPATH, "//*[@class='ivu-c-detailPart']/div[3]/div[4]/p").text.strip('"').strip()
       
        elif identifier_type == "ctr":
            arrival_datetime = driver.find_element(By.XPATH, "//*[@class='singleCNTRHead ivu-row']/div[2]//*[@class='date']").text.strip()
            # cannot get vessel name when searching by ctr number
            driver.find_element(By.CLASS_NAME, 'toggleCNTRMovingHistory').click()
            port_of_discharge = driver.find_element(By.XPATH, "//div[div[p[contains(., 'Discharged at Last POD')]]]/div[p[contains(.,'Location')]]/p[@class='value']").text.strip()

            # Extras (may use later)
            latest_status = driver.find_element(By.XPATH, "//div[p[contains(., 'Latest Status')]]/p[@class='value']").text.strip()
            latest_status_date = driver.find_element(By.XPATH, "//div[div[p[contains(., 'Latest Status')]]]/div/p[@class='data']").text.strip()
            latest_status_location = driver.find_element(By.XPATH, "//div[div[p[contains(., 'Latest Status')]]]/div[p[contains(.,'Location')]]/p[@class='value']").text.strip()

        arrival_date = None
        if arrival_datetime is not None:
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

        # restart_microservice()

        return jsonify(
            {
                "code": 500,
                "message": str(e)
            }
        ), 500
    
    finally:
        driver.close()

def restart_microservice():

    subprocess.call(['docker-compose','stop','scraper_cosco'])
    subprocess.call(['docker-compose', 'rm', '-f', 'scraper_cosco'])
    subprocess.call(['docker-compose', 'up', '-d', 'scraper_cosco'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8079, debug=True)