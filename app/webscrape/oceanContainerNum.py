from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

containerNum = "GAOU6627318"

try: 

    driver = webdriver.Chrome('/Users/varun/Downloads/chromedriver')

    driver.maximize_window()

    driver.get('https://sg.one-line.com/')

    time.sleep(3)

    print(driver.current_window_handle)

    print("First window title " + driver.title)

    driver.find_element(By.ID, "ctrack-field").send_keys(containerNum, Keys.ENTER)

    time.sleep(3)

    driver.switch_to.window(driver.window_handles[1])

    print("Second Window Title " + driver.title)

    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="headlessui-popover-panel-28"]/div/div[2]/div[3]/button[1]').click()

    driver.switch_to.frame("IframeCurrentEcom")

    status = driver.find_element(By.XPATH, '//*[@id="1"]/td[9]').text
    
    lastUpdatedTimeStamp = driver.find_element(By.XPATH, '//*[@id="1"]/td[8]').text

    driver.find_element(By.LINK_TEXT, containerNum).click()

    time.sleep(10)

    expectedArrivalTime = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[5]').text


finally:

    if expectedArrivalTime == None or lastUpdatedTimeStamp == None:

        print("No Status Found")

    else:

        time.sleep(3)

        print("ETA is: " + expectedArrivalTime[8:] + " and it is updated at " + lastUpdatedTimeStamp)

        print("Webscraping Complete")

