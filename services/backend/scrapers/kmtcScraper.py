#scraper related
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

#server related
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return("hello")

@app.route("/KMTC/<string:tracking_type>/<string:tracking_identifier>", methods=['GET'])
def track(tracking_type, tracking_identifier):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # init
    driver = webdriver.Chrome(options=options)



    # set max waiting time before throwing an exception
    driver.implicitly_wait(5)

    # landing page
    driver.get("https://www.ekmtc.com/index.html#/cargo-tracking")

    # iframe switch
    try:
        se = Select(driver.find_element("xpath", "//*[@id='frm']/div/table/tbody/tr/td[1]/select"))
        # query and results page
        if(tracking_type == "BL"):
            se.select_by_value("BL")
            # query
            # enter BL value
            driver.find_element(by=By.ID, value="blNo").send_keys(tracking_identifier)
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

        elif(tracking_type == "CTR"):
            se.select_by_value("CN")
            driver.find_element(by=By.ID, value="blNo").send_keys(tracking_identifier)
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

        return jsonify(
            {
                "code": 500,
                "message": str(e)
            }
        ), 500

    finally:
        driver.close()


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8082, debug=True) #to work as a local flask app