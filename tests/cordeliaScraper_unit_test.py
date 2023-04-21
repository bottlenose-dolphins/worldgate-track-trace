import unittest
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
sys.path.insert(0, '/worldgate-track-trace/services/backend/scrapers')
import Cordelia
from Cordelia import app


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
            tracking_identifier = "CSE23NSAPKG000274"
            expected_result = {
                "code": 200,
                "data": {
                    "status": "Empty On-Board",
                    "arrival_date": "16/02/2023 19:02",
                    "port_of_discharge": "Westport Kelang Multi Terminal (Kmt)",
                    "vessel_name": "Apollon D/Poll-02303E"
                }
            }
            result = Cordelia.track(tracking_type, tracking_identifier)
            result_dict = result.get_json()
            self.assertDictEqual(result_dict, expected_result)

    def test_track_CTR(self):
        with app.app_context():
        # test the CTR tracking type
            tracking_type = "CTR"
            tracking_identifier = "CSYU4021495"
            expected_result = {
                "code": 200,
                "data": {
                    "status": "Empty On-Board",
                    "arrival_date": "16/02/2023 19:02",
                    "port_of_discharge": "Westport Kelang Multi Terminal (Kmt)",
                    "vessel_name": "Apollon D/Poll-02303E"
                }
            }
            result = Cordelia.track(tracking_type, tracking_identifier)
            result_dict = result.get_json()
            self.assertDictEqual(result_dict, expected_result)

    def tearDown(self):
        # close the driver instance after each test
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()