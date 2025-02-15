from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import datetime
from .services import PricingService, load_pricing_config
from django.conf import settings
from django.core.cache import cache  # Import cache

class PricingServiceTests(TestCase):
    def setUp(self):
        # Clear the cache before each test
        cache.clear()
        # Reload pricing config so the changes are reflected in the test
        load_pricing_config()
        self.service = PricingService()


    def test_standard_fare_calculation(self):
        result = self.service.calculate_fare(
            distance=5,
            traffic_level='low',
            demand_level='normal'
        )
        self.assertEqual(result['traffic_multiplier'], Decimal('1.00'))
        self.assertEqual(result['demand_multiplier'], Decimal('1.00'))
        # Base fare (2.50) + distance fare (5 * 1.00) = 7.50
        self.assertEqual(result['total_fare'], Decimal('7.50'))

    def test_high_traffic_pricing(self):
        result = self.service.calculate_fare(
            distance=8,
            traffic_level='high',
            demand_level='normal'
        )
        self.assertEqual(result['traffic_multiplier'], Decimal('1.50'))
        # (Base fare (2.50) + distance fare (8 * 1.00)) * traffic multiplier (1.50) = 15.75
        self.assertEqual(result['total_fare'], Decimal('15.75'))

    def test_surge_pricing(self):
        result = self.service.calculate_fare(
            distance=12,
            traffic_level='normal',
            demand_level='peak'
        )
        self.assertEqual(result['demand_multiplier'], Decimal('1.80'))
        self.assertEqual(result['total_fare'], Decimal('32.62'))

    def test_peak_hour_with_high_traffic(self):
        # peak_time = datetime(2024, 2, 15, 17, 30)  # 5:30 PM
        result = self.service.calculate_fare(
            distance=7,
            traffic_level='high',
            demand_level='peak',
        )
        self.assertEqual(result['time_multiplier'], Decimal('1.00'))
        self.assertEqual(result['total_fare'], Decimal('25.65'))

class APITests(APITestCase):
    def setUp(self):
         # Clear the cache before each test
        cache.clear()
        # Reload pricing config so the changes are reflected in the test
        load_pricing_config()

    def test_calculate_fare_endpoint(self):
        url = reverse('calculate-fare')
        data = {
            'distance': 10,
            'traffic_level': 'high',
            'demand_level': 'peak'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_fare', response.data)

    def test_invalid_parameters(self):
        url = reverse('calculate-fare')
        data = {
            'distance': -1,  # Invalid distance
            'traffic_level': 'invalid',
            'demand_level': 'peak'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)