from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

class GeoApiTests(APITestCase):
    
    @patch('geo_api.services.requests.get')
    def test_unified_endpoint_success(self, mock_get):
        """Test that the API correctly combines and transforms data."""
        
        # 1. Mock the responses for both external APIs
        # This simulates what ip-api.com and restcountries.com return
        mock_get.side_effect = [
            # Mock Location API Response
            type('obj', (object,), {'json': lambda: {
                'status': 'success', 'country': 'Philippines', 'city': 'Manila', 'lat': 14.5, 'lon': 120.9
            }}),
            # Mock Population API Response
            type('obj', (object,), {'json': lambda: [{
                'population': 115000000, 'area': 300000, 'flags': {'png': 'https://flag.url'}
            }]})
        ]

        url = reverse('geo-insight-v1') + "?target=8.8.8.8"
        response = self.client.get(url)

        # 2. Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['country'], 'Philippines')
        
        # Check the transformation (Population Density calculation)
        # 115,000,000 / 300,000 = 383.33
        self.assertEqual(response.data['population_stats']['density_per_sq_km'], 383.33)

    def test_missing_parameter(self):
        """Test that the API returns 400 if 'target' is missing."""
        url = reverse('geo-insight-v1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
