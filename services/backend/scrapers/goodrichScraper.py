#scraper related
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import subprocess
from os import getenv

#server related
from flask import Flask, jsonify, request


app = Flask(__name__)

username = getenv("goodUsername")
password = getenv("goodPassword")

@app.route("/ping", methods=['GET'])
def ping():
    return("goodrich")

    # run with:
    # http://127.0.0.1:8081/GOOD/bl/VASSINCMB015609
    # http://127.0.0.1:8081/GOOD/ctr/VMLU3817377
@app.route("/good", methods=['POST'])
def track():

    options = Options()
    #https://stackoverflow.com/questions/53681161/why-puppeteer-needs-no-sandbox-to-launch-chrome-in-cloud-functions
    #'--no-sandbox' is needed, although it's more of a work around than a solution
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-dev-shm-usage')

    data = request.get_json()
    identifier = data["identifier"]
    identifier_type = data["identifier_type"]

    # # init
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=options)

    # set max waiting time before throwing an exception
    driver.implicitly_wait(5)
    
    # landing page
    driver.get("https://goodrich.co/track.php#new_tab")

    # iframe switch
    try:
        driver.switch_to.frame(driver.find_element(by=By.XPATH, value="/html/body/div[1]/iframe"))
        # username and password input elements
        eleUsername = driver.find_element(by=By.ID, value="UserId")
        elePassword = driver.find_element(by=By.ID, value="sPassword")

        # to replace value attribute w un&pw
        driver.execute_script("arguments[0].value ='" + username + "'", eleUsername)
        driver.execute_script("arguments[0].value ='" + password + "'", elePassword)

        # submit login credentials
        driver.find_element(by=By.XPATH, value="//*[@id=\"login\"]/div/input").click()
        # print("entered result page")
        
        # query and results page
        if(identifier_type == "ctr"):
            driver.find_element(by=By.XPATH, value="//*[@id=\"TAB1\"]/ul/li[2]/a").click()
            # query
            # enter ctr value
            driver.find_element(by=By.ID, value="ContainerNo").send_keys(identifier)
            # click search button
            driver.find_element(by=By.XPATH, value="//*[@id=\"TAB2\"]/div[1]/div/div[3]/input").click()
            
            port_of_discharge = driver.find_element(by=By.XPATH, value="//*[@id=\"table2id\"]/table[1]/tbody/tr[5]/td[5]").text.strip().title()
            vessel_name= driver.find_element(by=By.XPATH, value="//*[@id=\"table2id\"]/table[1]/tbody/tr[3]/td[2]").text.strip().title()
            status, arrival_datetime = driver.find_element(by=By.ID, value="fpodEtaId2").text.split(" : ")
        
        elif(identifier_type == "bl"):
            # query
            # enter bl value
            driver.find_element(by=By.ID, value="BlNo").send_keys(identifier)
            # click search button
            driver.find_element(by=By.XPATH, value=" //*[@id=\"TAB1\"]/div[1]/div/div[3]/input").click()
            
            port_of_discharge = driver.find_element(by=By.XPATH, value="//*[@id=\"table1id\"]/table[1]/tbody/tr[5]/td[5]").text.strip().title()
            vessel_name = driver.find_element(by=By.XPATH, value="//*[@id=\"table1id\"]/table[1]/tbody/tr[3]/td[2]").text.strip().title()
            status, arrival_datetime = driver.find_element(by=By.ID, value="fpodEtaId").text.split(" : ")

            # print(formatStatus)
            # print(est)
        
        arrival_date = arrival_datetime.split()[0]
        status = status.strip().title()
        return jsonify(
                {
                    "code": 200,
                    "data": {
                        "status": status,
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

    subprocess.call(['docker-compose','stop','scraper_good'])
    subprocess.call(['docker-compose', 'rm', '-f', 'scraper_good'])
    subprocess.call(['docker-compose', 'up', '-d', 'scraper_good'])


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=8081, debug=True) #to work as a local flask app