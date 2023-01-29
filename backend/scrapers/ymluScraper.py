from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# CTR Test
# identifier = "YMLU3434431"
# identifier_type = "ctr"

# BL Test
# identifier = "YMLUI450439005"
# identifier_type = "bl"

@app.route('/ymlu', methods=['POST'])
def ymluScraper():
    try:
        # Retrieve BL/Container information
        data = request.get_json()
        identifier = data["identifier"]
        identifier_type = data["identifier_type"]

        # Initialise chromedriver in headless mode
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        
        driver.get("https://www.yangming.com/e-service/Track_Trace/track_trace_cargo_tracking.aspx?rdolType=CT&str=" + identifier)
        time.sleep(2)
        
        # Check if identifier is a Container Number or B/L numberon
        if identifier_type == "bl":
            driver.find_element(By.ID, "ContentPlaceHolder1_rdolType_1").click()

            # Click on Track button to begin tracking
            driver.find_element(By.ID, "ContentPlaceHolder1_btnTrack").click()
            time.sleep(2)

        elif identifier_type == "ctr":
            # Click on Track button to begin tracking
            driver.find_element(By.ID, "ContentPlaceHolder1_btnTrack").click()
            time.sleep(2)

            # Click on View to see more info on the associated BL number
            driver.find_element(By.ID, "ContentPlaceHolder1_gvCargoTracking_lbtnView_0").click()
            time.sleep(2)
            
            # Click on BL number hyperlink to proceed to shipment information page
            driver.find_element(By.XPATH, '//*[@id="gvCargoTracking_Row_0"]/div/table/tbody/tr[1]/td/div/a').click()

        # Scrape shipment information
        arrival_date = driver.find_element(By.ID, "ContentPlaceHolder1_rptBLNo_rptRoutingSchedule_0_lblDateTime_1").text
        port_of_discharge = driver.find_element(By.ID, "ContentPlaceHolder1_rptBLNo_gvBasicInformation_0_lblDischarge_0").text
        vessel_name = driver.find_element(By.XPATH, "//a[@title='Click here to view vessel schedule']").text

        if arrival_date != None:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "arrival_date": arrival_date,
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
        
if __name__ == '__main__':
    app.run(port=8080, debug=True)
    