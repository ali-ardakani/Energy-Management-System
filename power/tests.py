from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

class DemandReportTestCase(APITestCase):
    def test_create(self):
        data = {
            "demand": [
                {
                    "date": "2020-04-01",
                    "hour": 1,
                    "market_demand": 1,
                    "ontario_demand": 1
                },
                {
                    "date": "2020-04-01",
                    "hour": 2,
                    "market_demand": 2,
                    "ontario_demand": 2
                },
                {
                    "date": "2020-04-01",
                    "hour": 3,
                    "market_demand": 3,
                    "ontario_demand": 3
                }
            ]
        }
        response = self.client.post('/api/demand', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_delete(self):
        data = {
            "demand": [
                {
                    "date": "2020-04-01",
                    "hour": 1,
                    "market_demand": 1,
                    "ontario_demand": 1
                },
                {
                    "date": "2020-04-01",
                    "hour": 2,
                    "market_demand": 2,
                    "ontario_demand": 2
                },
                {
                    "date": "2020-04-01",
                    "hour": 3,
                    "market_demand": 3,
                    "ontario_demand": 3
                }
            ]
        }
        response = self.client.post('/api/demand', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete('/api/demand?date=2020-04-01')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get(self):
        data = {
            "demand": [
                {
                    "date": "2020-04-01",
                    "hour": 1,
                    "market_demand": 1,
                    "ontario_demand": 1
                },
                {
                    "date": "2020-05-01",
                    "hour": 2,
                    "market_demand": 2,
                    "ontario_demand": 2
                },
                {
                    "date": "2020-06-01",
                    "hour": 3,
                    "market_demand": 3,
                    "ontario_demand": 3
                }
            ]
        }
        response = self.client.post('/api/demand', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/api/demand?start=2020-04-01&end=2020-06-01')
        self.assertEqual(len(response.data), 3)