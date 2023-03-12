import sys
sys.path.insert(1, '/worldgate-track-trace/services/backend/core')
import complex_scraper
from complex_scraper import app
import unittest
import requests
import json

class TestComplexScraper(unittest.TestCase):
    def setUp(self):
        # Start the Flask app for testing
        self.app = app.test_client()

    def test_scraper_with_ctr(self):
        # Send a POST request to the endpoint with a CTR identifier
        payload = {
            "shipping_line": "Yang Ming",
            "identifier": "YMLU3434431",
            "identifier_type": "ctr",
            "direction": "export"
        }
        response = self.app.post('/scrape', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check that the response data is as expected
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['arrival_date'], "2022/12/16")
        self.assertEqual(data['data']['port_of_discharge'], "HONGKONG (HKHKG)")
        self.assertEqual(data['data']['vessel_name'], "YM CONSTANCY")

if __name__ == '__main__':
    unittest.main()