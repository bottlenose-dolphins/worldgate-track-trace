import sys
sys.path.insert(0, '/worldgate-track-trace/services/backend/scrapers')
import ymlu_scraper
from ymlu_scraper import app
import unittest
import requests
import json

class TestYmluScraper(unittest.TestCase):
    def setUp(self):
        # Start the Flask app for testing
        self.app = app.test_client()

    def test_scraper_with_ctr(self):
        # Send a POST request to the endpoint with a CTR identifier
        payload = {
            "identifier": "YMLU3434431",
            "identifier_type": "ctr"
        }
        response = self.app.post('/ymlu', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check that the response data is as expected
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['arrival_date'], "2022/12/16")
        self.assertEqual(data['data']['port_of_discharge'], "HONGKONG (HKHKG)")
        self.assertEqual(data['data']['vessel_name'], "YM CONSTANCY")

    def test_scraper_with_bl(self):
        # Send a POST request to the endpoint with a BL identifier
        payload = {
            "identifier": "YMLUI450439005",
            "identifier_type": "bl"
        }
        response = self.app.post('/ymlu', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check that the response data is as expected
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['arrival_date'], "2022/12/16")
        self.assertEqual(data['data']['port_of_discharge'], "HONGKONG (HKHKG)")
        self.assertEqual(data['data']['vessel_name'], "YM CONSTANCY")

if __name__ == '__main__':
    unittest.main()