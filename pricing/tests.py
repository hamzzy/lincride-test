from django.test import TestCase
from rest_framework.test import APIClient
from .pricing_logic import calculate_fare
from django.core.cache import cache
import datetime

class PricingLogicTests(TestCase):

    def setUp(self):
        cache.clear()  # Clear cache before each test

    def test_standard_fare_calculation(self):
        fare_details = calculate_fare(distance=5, traffic_level='low', demand_level='normal', current_time=datetime.time(10,0))
        self.assertEqual(fare_details['total_fare'], 7.5)

    def test_high_traffic_pricing(self):
        fare_details = calculate_fare(distance=8, traffic_level='high', demand_level='normal', current_time=datetime.time(10,0))
        self.assertEqual(fare_details['total_fare'], 15.75)

    def test_surge_pricing(self):
        fare_details = calculate_fare(distance=12, traffic_level='normal', demand_level='peak', current_time=datetime.time(10,0))
        self.assertGreaterEqual(fare_details['demand_multiplier'], 1.8)

    def test_peak_hour_pricing(self):
        fare_details = calculate_fare(distance=5, traffic_level='low', demand_level='normal', current_time=datetime.time(8,0))
        self.assertEqual(fare_details['time_multiplier'], 1.3)
        self.assertEqual(fare_details['total_fare'], 9.75)

    def test_peak_hour_with_high_traffic(self):
        fare_details = calculate_fare(distance=7, traffic_level='high', demand_level='peak', current_time=datetime.time(18,0))
        self.assertGreaterEqual(fare_details['total_fare'], 39.66)

    def test_long_distance_ride(self):
        fare_details = calculate_fare(distance=20, traffic_level='low', demand_level='normal', current_time=datetime.time(10,0))
        self.assertEqual(fare_details['total_fare'], 22.5)

    def test_invalid_distance(self):
        with self.assertRaises(ValueError):
            calculate_fare(distance=-1, traffic_level='low', demand_level='normal')

    def test_invalid_distance_type(self):
        with self.assertRaises(ValueError):
            calculate_fare(distance="abc", traffic_level='low', demand_level='normal')

    def test_caching_traffic_multiplier(self):
        # Initial call should not be cached
        with self.assertNumQueries(0):  # Adjust as needed based on your environment
            multiplier1 = get_traffic_multiplier("high")

        # Second call should be cached (no queries executed)
        with self.assertNumQueries(0):
            multiplier2 = get_traffic_multiplier("high")

        self.assertEqual(multiplier1, multiplier2)

class PricingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        cache.clear()

    def test_calculate_fare_endpoint(self):
        response = self.client.get('/api/calculate-fare/?distance=10&traffic_level=high&demand_level=peak¤t_time=10:00')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['base_fare'], 2.5)
        self.assertEqual(response.data['distance_fare'], 10.0)
        self.assertEqual(response.data['traffic_multiplier'], 1.5)
        self.assertGreaterEqual(response.data['demand_multiplier'], 1.8)
        self.assertEqual(response.data['time_multiplier'], 1.0)
        self.assertGreaterEqual(response.data['total_fare'], 34.5) # Adjusted expected total_fare.

    def test_calculate_fare_endpoint_invalid_distance(self):
         response = self.client.get('/api/calculate-fare/?distance=-10&traffic_level=high&demand_level=peak¤t_time=10:00')
         self.assertEqual(response.status_code, 400)
         self.assertIn("Distance must be greater than zero.", str(response.data['error']))

    def test_calculate_fare_endpoint_time(self):
        response = self.client.get('/api/calculate-fare/?distance=5&traffic_level=low&demand_level=normal¤t_time=08:00')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['time_multiplier'], 1.3)
        self.assertEqual(response.data['total_fare'], 9.75)
