
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#server related
# server related
from flask import Flask, jsonify

import time

username = ""
password = ""
app = Flask(__name__)

@app.route("/CCSL/<string:tracking_type>/<string:tracking_identifier>", methods=['GET'])
def track(tracking_type, tracking_identifier):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # init
    driver = webdriver.Chrome(options=options)

    # set max waiting time before throwing an exception
    driver.implicitly_wait(5)
    
    # landing page
    driver.get("https://www.cordelialine.com/login-and-registration/")

    try:
      
        # username and password input elements
        eleUsername = driver.find_element(by=By.ID, value="erf_username")
        elePassword = driver.find_element(by=By.ID, value="erf_password")

        # to replace value attribute w un&pw
        driver.execute_script("arguments[0].value ='" + username + "'", eleUsername)
        driver.execute_script("arguments[0].value ='" + password + "'", elePassword)

        # submit login credentials
        driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div/div/div/div[1]/div/div/div[1]/form[1]/div[7]/div/button").click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")     
        # query and results page
        if(tracking_type == "BL"):
            driver.get("https://www.cordelialine.com/bltracking/?blno="+tracking_identifier)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")     


            port_of_discharge = driver.find_element(by=By.XPATH, value="//*[@id='checkShedTable1']/tbody/tr/td[1]").text.strip().title()
            vessel_name = driver.find_element(by=By.XPATH, value="//*[@id='checkShedTable']/tbody/tr/td[5]").text.strip().title()
            status = driver.find_element(by=By.XPATH, value="//*[@id='checkShedTable1']/tbody/tr/td[12]").text.strip().title()
            arrival_datetime = driver.find_element(by=By.XPATH, value="//*[@id='checkShedTable1']/tbody/tr/td[2]").text.strip().title()

        elif(tracking_type == "CTR"):
            driver.get("https://www.cordelialine.com/container-tracking/?contno="+tracking_identifier)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            
            port_of_discharge = driver.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div/div/section/table[2]/tbody/tr/td[1]").text.strip().title()
            vessel_name = driver.find_element(by=By.XPATH, value="//*[@id=\"checkShedTable1\"]/tbody/tr/td[6]").text.strip().title()
            status=driver.find_element(by=By.XPATH, value="//*[@id=\"checkShedTable1\"]/tbody/tr/td[12]").text.strip().title()
            arrival_datetime = driver.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div/div/section/table[2]/tbody/tr/td[2]").text.strip().title()
      
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
            })
    finally:
        driver.close()
        
    
if __name__ == '__main__':
    app.run(port=5004, debug=True)
