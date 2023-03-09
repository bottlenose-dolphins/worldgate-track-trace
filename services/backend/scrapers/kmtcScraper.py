#scraper related
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import subprocess
from flask_cors import CORS

#server related
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://worldgatetracktrace.click, http://127.0.0.1"}})

@app.route("/ping", methods=['GET'])
def ping():
    return("hello")

@app.route("/kmtc", methods=['POST'])
def track():

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # init
    driver = webdriver.Chrome(options=options)

    data = request.get_json()
    identifier = data["identifier"]
    identifier_type = data["identifier_type"]

    # set max waiting time before throwing an exception
    driver.implicitly_wait(5)

    # landing page
    driver.get("https://www.ekmtc.com/index.html#/cargo-tracking")

    # iframe switch
    try:
        se = Select(driver.find_element("xpath", "//*[@id='frm']/div/table/tbody/tr/td[1]/select"))
        # query and results page
        if(identifier_type == "bl"):
            se.select_by_value("BL")
            # query
            # enter BL value
            driver.find_element(by=By.ID, value="blNo").send_keys(identifier)
            # click search button
            driver.find_element(by=By.XPATH, value="//*[@id='frm']/div/table/tbody/tr/td[3]/a").click()
            time.sleep(5)

            port_of_discharge = driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[5]").text.strip().title()
            port_of_discharge = port_of_discharge[:port_of_discharge.index('\n')]
            vessel_name= driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[7]").text.strip().title()
            vessel_name = vessel_name[vessel_name.index(')')+1:]
            status=driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[8]/span").text.strip().title()
            arrival_datetime = driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[6]").text.strip().title()
            arrival_datetime = arrival_datetime[arrival_datetime.index('\n')+1:]

        elif(identifier_type == "ctr"):
            se.select_by_value("CN")
            driver.find_element(by=By.ID, value="blNo").send_keys(identifier)
            driver.find_element(by=By.XPATH, value="//*[@id='frm']/div/table/tbody/tr/td[3]/a").click()
            time.sleep(5)

            port_of_discharge = driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[5]").text.strip().title()
            port_of_discharge = port_of_discharge[:port_of_discharge.index('\n')]
            vessel_name= driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[7]").text.strip().title()
            vessel_name = vessel_name[vessel_name.index(')')+1:]
            status=driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[8]/span").text.strip().title()
            arrival_datetime = driver.find_element(by=By.XPATH, value="//*[@id='frm']/div[2]/table/tbody/tr/td[6]").text.strip().title()
            arrival_datetime = arrival_datetime[arrival_datetime.index('\n')+1:]

        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "status": status,
                        "arrival_date": arrival_datetime,
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

    subprocess.call(['docker-compose','stop','scraper_kmtc'])
    subprocess.call(['docker-compose', 'rm', '-f', 'scraper_kmtc'])
    subprocess.call(['docker-compose', 'up', '-d', 'scraper_kmtc'])


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8082, debug=True) #to work as a local flask app