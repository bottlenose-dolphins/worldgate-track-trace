from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

# driver (either first 2 or third)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary

# creds
from creds.goodrich import username
from creds.goodrich import password

options = Options()
options.headless = True

# init
# driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver = webdriver.Chrome(options=options)


# set max waiting time before throwing an exception
driver.implicitly_wait(5)
# for executing javascript
action = ActionChains(driver)

bl = "VASSINCMB015609"


# landing page
driver.get("https://goodrich.co/track.php#new_tab")
# print("reachedLandingSite")

# iframe switch
driver.switch_to.frame(driver.find_element(
    by=By.XPATH, value="/html/body/div[1]/iframe"))

# username and password input elements
eleUsername = driver.find_element(by=By.XPATH, value="//*[@id=\"UserId\"]")
elePassword = driver.find_element(by=By.XPATH, value="//*[@id=\"sPassword\"]")

# to replace value attribute w un&pw
driver.execute_script("arguments[0].value ='" + username + "'", eleUsername)
driver.execute_script("arguments[0].value ='" + password + "'", elePassword)

# submit login credentials
driver.find_element(by=By.XPATH, value="//*[@id=\"login\"]/div/input").click()
# print("entered result page")

# query and results page

# query
# enter BL value
driver.find_element(by=By.XPATH, value="//*[@id=\"BlNo\"]").send_keys(bl)
# click search button
driver.find_element(
    by=By.XPATH, value="//*[@id=\"TAB1\"]/div[1]/div/div[3]/input").click()

# results
try:
    destinationPort = driver.find_element(
        by=By.XPATH, value="//*[@id=\"fpodId\"]").text.strip().title()
    # print(destinationPort)
    vesselName = driver.find_element(
        by=By.XPATH, value="//*[@id=\"table1id\"]/table[1]/tbody/tr[3]/td[2]").text.strip().title()
    # print(vesselName)

    status, est = driver.find_element(
        by=By.XPATH, value="//*[@id=\"fpodEtaId\"]").text.split(" : ")
    formatStatus = status.strip().title()

    # print(formatStatus)
    # print(est)

    if formatStatus == "Arrived":
        print("Status of your query : " + formatStatus + ". It traveled on the" +
              vesselName + " and it reached " + destinationPort + " on " + est)

    # Unsure on wording
    elif formatStatus == "Arriving":
        print("Status of your query : " + formatStatus + ". It is traveling on the" +
              vesselName + " and it is reaching " + destinationPort + " on " + est)

    else:
        print("Status could not be determined")

except:
    print("Failed to obtain / missing info")

finally:
    # print("fin")
    driver.quit()
