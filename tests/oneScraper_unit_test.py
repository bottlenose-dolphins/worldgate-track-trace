import unittest
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
sys.path.insert(1, '/worldgate-track-trace/services/backend/scrapers')
import oneScraper
from oneScraper import app


class TestWebScraper(unittest.TestCase):

    def setUp(self):
        # set up a Chrome driver instance
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=self.options)

    def test_track_BL(self):
        with app.app_context():
        # test the BL tracking type
            tracking_type = "BL"
            tracking_identifier = "ONEYSINC72210300"
            expected_result = {
                "code": 200,
                "data": {
                    "status": "Vessel Departure from Port of Loading",
                    "time_of_arrival": "2023-02-18 08:30",
                    "port_of_discharge": "HAMBURG, HH, GERMANY",
                    "vessel_name": "ONE TRIBUTE 020W (TIRT)"
                }
            }
            result = oneScraper.oneScraper(tracking_type, tracking_identifier)
            result_dict = result.get_json()
            self.assertDictEqual(result_dict, expected_result)

    def test_track_CTR(self):
        with app.app_context():
        # test the CTR tracking type
            tracking_type = "CTR"
            tracking_identifier = "GAOU6627318"
            expected_result = {
                "code": 200,
                "data": {
                    "status": "Gate Out from Inbound Terminal for Delivery to Consignee (or Port Shuttle)",
                    "time_of_arrival": "023-01-31 02:30",
                    "port_of_discharge": "HAMBURG, HH, GERMANY",
                    "vessel_name": "YM WELLNESS 033W (WLLT)"
                }
            }
            result = oneScraper.oneScraper(tracking_type, tracking_identifier)
            result_dict = result.get_json()
            self.assertDictEqual(result_dict, expected_result)

    def tearDown(self):
        # close the driver instance after each test
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()