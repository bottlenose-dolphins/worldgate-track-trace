from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time

containerNum = "GAOU6627318"
blNum = "SINC72210300"

try:

    options = Options()

    options.headless = True

    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    driver.get('https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking?ctrack-field=' + containerNum + '&trakNoParam=' + containerNum)

    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="headlessui-popover-panel-28"]/div/div[2]/div[3]/button[1]').click()

    driver.switch_to.frame("IframeCurrentEcom")

    status = driver.find_element(By.XPATH, '//*[@id="1"]/td[9]').text
    
    driver.find_element(By.XPATH, '//*[@id="1"]/td[4]/a').click()

    time.sleep(10)

    expectedArrivalTime = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[5]').text

    destinationPort = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[4]').text

    vesselName = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[1]').text


finally:

    if expectedArrivalTime == None or lastUpdatedTimeStamp == None:

        print("No Status Found")

    else:

        time.sleep(3)

        print("Status of your query : " + status + ". It is travelling on " + vesselName + " and it will reach " + destinationPort + " at " + expectedArrivalTime[8:])

        print("Webscraping Complete")

