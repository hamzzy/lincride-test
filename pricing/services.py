import logging
import asyncio
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

def load_pricing_config():
    """Loads pricing configuration from cache or provides defaults."""
    try:
      
            default_config = {
                'BASE_FARE': Decimal('2.50'),
                'PER_KM_RATE': Decimal('1.00'),
                'TRAFFIC_MULTIPLIERS': {
                    'low': Decimal('1.00'),
                    'normal': Decimal('1.25'),
                    'high': Decimal('1.50')
                },
                'DEMAND_MULTIPLIERS': {
                    'low': Decimal('0.90'),
                    'normal': Decimal('1.00'),
                    'peak': Decimal('1.80')
                },
                'PEAK_HOUR_MULTIPLIER': Decimal('1.30')
            }
            # await asyncio.to_thread(settings.CACHE.set, 'pricing_config', default_config, timeout=None)
            return default_config
    except Exception as e:
        logger.exception("Error loading pricing config")
        # Provide a fallback, potentially raise an exception
        return {  # Very basic fallback
            'BASE_FARE': Decimal('2.50'),
            'PER_KM_RATE': Decimal('1.00'),
            'TRAFFIC_MULTIPLIERS': {'low': Decimal('1.00'), 'normal': Decimal('1.00'), 'high': Decimal('1.00')},
            'DEMAND_MULTIPLIERS': {'low': Decimal('1.00'), 'normal': Decimal('1.00'), 'peak': Decimal('1.00')},
            'PEAK_HOUR_MULTIPLIER': Decimal('1.00')
        }

PRICING_CONFIG = load_pricing_config()

class PricingService:
    def __init__(self):
        self.pricing_config = PRICING_CONFIG

    def get_traffic_multiplier(self, traffic_level: str) -> Decimal:
        return self.pricing_config['TRAFFIC_MULTIPLIERS'].get(
            traffic_level,
            self.pricing_config['TRAFFIC_MULTIPLIERS']['normal']
        )

    def get_demand_multiplier(self, demand_level: str) -> Decimal:
        return self.pricing_config['DEMAND_MULTIPLIERS'].get(
            demand_level,
            self.pricing_config['DEMAND_MULTIPLIERS']['normal']
        )

    def is_peak_hour(self, time: datetime) -> bool:
        hour = time.hour
        return 7 <= hour <= 9 or 16 <= hour <= 19

    def calculate_fare(self, distance: float, traffic_level: str,
                      demand_level: str, time: datetime = None) -> dict:
        """Calculates the fare based on distance, traffic, demand, and time."""
        try:
            if time is None:
                time = datetime.now()

            # Calculate base components
            base_fare = self.pricing_config['BASE_FARE']
            distance_fare = Decimal(str(distance)) * self.pricing_config['PER_KM_RATE']

            # Apply multipliers
            traffic_multiplier = self.get_traffic_multiplier(traffic_level)
            demand_multiplier = self.get_demand_multiplier(demand_level)
            time_multiplier = (self.pricing_config['PEAK_HOUR_MULTIPLIER']
                              if self.is_peak_hour(time) else Decimal('1.00'))

            # Calculate total fare
            subtotal = (base_fare + distance_fare)
            total_fare = subtotal * traffic_multiplier * demand_multiplier * time_multiplier

            fare_details = {
                'base_fare': base_fare,
                'distance_fare': distance_fare,
                'traffic_multiplier': traffic_multiplier,
                'demand_multiplier': demand_multiplier,
                'time_multiplier': time_multiplier,
                'total_fare': total_fare.quantize(Decimal('0.01'))
            }
            logger.debug(f"Fare calculated: {fare_details}")
            return fare_details
        except Exception as e:
            logger.exception("Error during fare calculation")
            raise # Re-raise the exception to be handled in the view