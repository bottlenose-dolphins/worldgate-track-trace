from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

blNum = "SINC69412601"

try: 

    driver = webdriver.Chrome('/Users/varun/Downloads/chromedriver')

    driver.maximize_window()

    driver.get('https://sg.one-line.com/')

    time.sleep(3)

    print(driver.current_window_handle)

    print("First window title " + driver.title)

    driver.find_element(By.ID, "ctrack-field").send_keys(blNum, Keys.ENTER)

    time.sleep(3)

    driver.switch_to.window(driver.window_handles[1])

    print("Second Window Title " + driver.title)

    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="headlessui-popover-panel-28"]/div/div[2]/div[3]/button[1]').click()

    driver.switch_to.frame("IframeCurrentEcom")

    eventDate = driver.find_element(By.XPATH, '//*[@id="1"]/td[8]').text

    status = driver.find_element(By.XPATH, '//*[@id="1"]/td[9]').text

    time.sleep(3)

finally:

    if eventDate == None or status == None:

        print("No Status Found")

    else:

        time.sleep(3)

        print("Status is: " + status + " and it is updated at " + eventDate)

        print("Webscraping Complete")

