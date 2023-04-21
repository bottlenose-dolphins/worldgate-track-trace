import sys
sys.path.insert(0, '/worldgate-track-trace/services/backend/scrapers')
import coscoScraper
from coscoScraper import app
import unittest
import requests
import json

class TestCoscoScraper(unittest.TestCase):
    def setUp(self):
        # Start the Flask app for testing
        self.app = app.test_client()

    def test_scraper_with_ctr(self):
        # Send a POST request to the endpoint with a CTR identifier
        payload = {
            "identifier": "OOLU4299134",
            "identifier_type": "ctr"
        }
        response = self.app.post('/cosco', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check that the response data is as expected
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['arrival_date'], "2023-01-24")
        self.assertEqual(data['data']['port_of_discharge'], "Bharat Mumbai Ctn Tmls Private Ltd,Nhava Sheva,Maharashtra,India")
        self.assertEqual(data['data']['vessel_name'], None)

    def test_scraper_with_bl(self):
        # Send a POST request to the endpoint with a BL identifier
        payload = {
            "identifier": "COAU7242927890",
            "identifier_type": "bl"
        }
        response = self.app.post('/cosco', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check that the response data is as expected
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['arrival_date'], "2023-01-24")
        self.assertEqual(data['data']['port_of_discharge'], "Nhava Sheva-Bharat Mumbai Ctn Tmls Private Ltd")
        self.assertEqual(data['data']['vessel_name'], "SEAMAX WESTPORT")

if __name__ == '__main__':
    unittest.main()