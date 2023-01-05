from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

identifier = "GAOU6627318"

try:

    # headless mode will run the webscraping in the background and lesser RAM will be utilised --> Much more efficient process

    options = Options()

    options.headless = True

    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

    # Can interchange identifier with Container/BL Number as the process is similar

    driver.get('https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking?ctrack-field=' + identifier + '&trakNoParam=' + identifier)

    time.sleep(3)

    # pop-up present when querying for status in the page so need to click "Skip"

    driver.find_element(By.XPATH, '//*[@id="headlessui-popover-panel-28"]/div/div[2]/div[3]/button[1]').click()

    # Inline Frame present so need to change to this so you can extract values

    driver.switch_to.frame("IframeCurrentEcom")

    status = driver.find_element(By.XPATH, '//*[@id="1"]/td[9]').text

    #clicking the Container Number will show us more details like Port of Destination and ETA

    driver.find_element(By.XPATH, '//*[@id="1"]/td[4]/a').click()

    time.sleep(10)

    expectedArrivalTime = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[5]').text

    destinationPort = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[4]').text

    vesselName = driver.find_element(By.XPATH, '//*[@id="sailing"]/tbody/tr/td[1]').text


finally:

    if status == None:

        print("No Status Found")

    else:

        time.sleep(3)

        print("Status of your query : " + status + ". It is travelling on " + vesselName + " and it will reach " + destinationPort + " at " + expectedArrivalTime[8:])

        print("Webscraping Complete")

