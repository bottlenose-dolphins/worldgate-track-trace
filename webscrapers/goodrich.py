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

#swagger related
# SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
# API_URL = 'backend/microservices/docs/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
#     API_URL,
#     config={  # Swagger UI config overrides
#         'app_name': "esgTest"
#     },
#     # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
#     #    'clientId': "your-client-id",
#     #    'clientSecret': "your-client-secret-if-required",
#     #    'realm': "your-realms",
#     #    'appName': "your-app-name",
#     #    'scopeSeparator': " ",
#     #    'additionalQueryStringParams': {'test': "hello"}
#     # }
# )

# app.register_blueprint(swaggerui_blueprint)

@app.route("/ping", methods=['GET'])
def ping():
    return("hello")


@app.route("/GOOD/<string:tracking_type>/<string:tracking_identifier>", methods=['GET'])
def track(tracking_type, tracking_identifier):

    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.headless = True

    # init
    # driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver = webdriver.Chrome(options=options)

    # http://127.0.0.1:5001/GOOD/BL/VASSINCMB015609
    # http://127.0.0.1:5001/GOOD/CTR/VMLU3817377
  

    # set max waiting time before throwing an exception
    driver.implicitly_wait(5)
    # for executing javascript
    action = ActionChains(driver)
   
    # landing page
    driver.get("https://goodrich.co/track.php#new_tab")
    # print("reachedLandingSite")

    # iframe switch
    try:
        driver.switch_to.frame(driver.find_element(
            by=By.XPATH, value="/html/body/div[1]/iframe"))
    except NoSuchElementException:
        pass
    # username and password input elements
    eleUsername = driver.find_element(by=By.XPATH, value="//*[@id=\"UserId\"]")
    elePassword = driver.find_element(by=By.XPATH, value="//*[@id=\"sPassword\"]")

    # to replace value attribute w un&pw
    driver.execute_script("arguments[0].value ='" + username + "'", eleUsername)
    driver.execute_script("arguments[0].value ='" + password + "'", elePassword)

    # submit login credentials
    driver.find_element(by=By.XPATH, value="//*[@id=\"login\"]/div/input").click()
    # print("entered result page")

    try:

        # query and results page
        if(tracking_type == "CTR"):
            driver.find_element(by=By.XPATH, value="//*[@id=\"TAB1\"]/ul/li[2]/a").click()
            # query
            # enter CTR value
            driver.find_element(by=By.XPATH, value="//*[@id=\"ContainerNo\"]").send_keys(tracking_identifier)
            # click search button
            driver.find_element(by=By.XPATH, value="//*[@id=\"TAB2\"]/div[1]/div/div[3]/input").click()

            destinationPort = driver.find_element(by=By.XPATH, value="//*[@id=\"fpodId2\"]").text.strip().title()
            # print(destinationPort)
            vesselName = driver.find_element(by=By.XPATH, value="//*[@id=\"table2id\"]/table[1]/tbody/tr[3]/td[2]").text.strip().title()
            # print(vesselName)

            status, est = driver.find_element(by=By.XPATH, value="//*[@id=\"fpodEtaId2\"]").text.split(" : ")
            formatStatus = status.strip().title()
    

            
        else:
            # query
            # enter BL value
            driver.find_element(by=By.XPATH, value="//*[@id=\"BlNo\"]").send_keys(tracking_identifier)
            # click search button
            driver.find_element(by=By.XPATH, value=" //*[@id=\"TAB1\"]/div[1]/div/div[3]/input").click()

            destinationPort = driver.find_element(
            by=By.XPATH, value="//*[@id=\"fpodId\"]").text.strip().title()
        # print(destinationPort)
            vesselName = driver.find_element(
                by=By.XPATH, value="//*[@id=\"table1id\"]/table[1]/tbody/tr[3]/td[2]").text.strip().title()
            # print(vesselName)

            status, est = driver.find_element(by=By.XPATH, value="//*[@id=\"fpodEtaId\"]").text.split(" : ")
            formatStatus = status.strip().title()

            # print(formatStatus)
            # print(est)

        if formatStatus == "Arrived":
            return("Status of your query : " + formatStatus + ". It traveled on the " +
                vesselName + " and it reached " + destinationPort + " on " + est)

        # Unsure on wording
        elif formatStatus == "Arriving":
            return("Status of your query : " + formatStatus + ". It is traveling on the " +
                vesselName + " and it is reaching " + destinationPort + " on " + est)

        else:
            print("Status could not be determined")

    except:
        return("failed")
        print("Failed to obtain / missing info")
    
    finally:
        # print("fin")
        driver.quit()


if __name__ == '__main__':
    app.run(port=5002, debug=True)
