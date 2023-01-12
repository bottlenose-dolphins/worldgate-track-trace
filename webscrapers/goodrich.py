#scraper related
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

#exceptions from selenium 
from selenium.common.exceptions import NoSuchElementException

# driver management (either first 2 or third)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary

#server related
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

#logging
import logging

# creds
from creds.goodrich import username
from creds.goodrich import password

app = Flask(__name__)
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["2000 per day", "500 per hour"]
# )

CORS(app)

@app.route("/ping", methods=['GET'])
def ping():
    return("hello")


@app.route("/GOOD/<string:tracking_type>/<string:tracking_identifier>", methods=['GET'])
def track(tracking_type, tracking_identifier):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # init
    # driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(options=options)

    # run with:
    # http://127.0.0.1:5003/GOOD/BL/VASSINCMB015609
    # http://127.0.0.1:5003/GOOD/CTR/VMLU3817377

    # set max waiting time before throwing an exception
    driver.implicitly_wait(5)
    # for executing javascript
    action = ActionChains(driver)
    
    # landing page
    driver.get("https://goodrich.co/track.php#new_tab")
    # print("reachedLandingSite")

    # iframe switch
    try:
        driver.switch_to.frame(driver.find_element(by=By.XPATH, value="/html/body/div[1]/iframe"))
        # username and password input elements
        eleUsername = driver.find_element(by=By.XPATH, value="//*[@id=\"UserId\"]")
        elePassword = driver.find_element(by=By.XPATH, value="//*[@id=\"sPassword\"]")

        # to replace value attribute w un&pw
        driver.execute_script("arguments[0].value ='" + username + "'", eleUsername)
        driver.execute_script("arguments[0].value ='" + password + "'", elePassword)

        # submit login credentials
        driver.find_element(by=By.XPATH, value="//*[@id=\"login\"]/div/input").click()
        # print("entered result page")
    
    except:
        return("failed to login")
    
    try:
        # query and results page
        if(tracking_type == "CTR"):
            driver.find_element(by=By.XPATH, value="//*[@id=\"TAB1\"]/ul/li[2]/a").click()
            # query
            # enter CTR value
            driver.find_element(by=By.XPATH, value="//*[@id=\"ContainerNo\"]").send_keys(tracking_identifier)
            # click search button
            driver.find_element(by=By.XPATH, value="//*[@id=\"TAB2\"]/div[1]/div/div[3]/input").click()
            
            destinationPort = driver.find_element(by=By.XPATH, value="//*[@id=\"fpodId2\"]").get_attribute("innerHTML").strip().title()
            # print(destinationPort)
            # driver.execute_script("window.scrollBy(0,500)","")
            vesselName = driver.find_element(by=By.XPATH, value="//*[@id=\"table2id\"]/table[1]/tbody/tr[5]/td[5]").text.strip().title()
            # print(vesselName)
            status, est = driver.find_element(by=By.XPATH, value="//*[@id=\"fpodEtaId2\"]").text.split(" : ")
            formatStatus = status.strip().title()

        else:
            # query
            # enter BL value
            driver.find_element(by=By.XPATH, value="//*[@id=\"BlNo\"]").send_keys(tracking_identifier)
            # click search button
            driver.find_element(by=By.XPATH, value=" //*[@id=\"TAB1\"]/div[1]/div/div[3]/input").click()
            destinationPort = driver.find_element(by=By.XPATH, value="//*[@id=\"fpodId\"]").text.strip().title()
            # print(destinationPort)
            vesselName = driver.find_element(by=By.XPATH, value="//*[@id=\"table1id\"]/table[1]/tbody/tr[3]/td[2]").text.strip().title()
            # print(vesselName)
            status, est = driver.find_element(by=By.XPATH, value="//*[@id=\"fpodEtaId\"]").text.split(" : ")
            formatStatus = status.strip().title()

            # print(formatStatus)
            # print(est)

        if formatStatus == "Arrived":
            return("Status of your query : " + formatStatus + ". It arrived at " + destinationPort + " on " + est)

        # Unsure on wording
        elif formatStatus == "Arriving":
            return("Status of your query : " + formatStatus + ". It arrived at " + destinationPort + " on " + est)

        else:
            return("Status could not be determined")

    except:
        return("failed to obtain results")
    
    finally:
        driver.close()


if __name__ == '__main__':
    app.run(port=5003, debug=True)
