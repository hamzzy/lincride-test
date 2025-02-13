import datetime
from django.core.cache import cache

BASE_FARE = 2.5
PER_KM_RATE = 1.0

def calculate_fare(distance, traffic_level, demand_level, current_time=None):
    """
    Calculates the ride fare based on dynamic pricing factors,
    using caching and a more sophisticated surge pricing based on recent requests.
    """

    if not isinstance(distance, (int, float)):
        raise ValueError("Distance must be a number.")
    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")

    base_fare = BASE_FARE
    distance_fare = distance * PER_KM_RATE

    traffic_multiplier = get_traffic_multiplier(traffic_level)
    demand_multiplier = get_demand_multiplier(demand_level) # Original get_demand_multiplier removed.

    # Sophisticated Demand Surge Pricing
    demand_multiplier = calculate_realtime_surge(demand_level)

    # Time of day multiplier
    time_multiplier = get_time_multiplier(current_time)

    total_fare = (base_fare + distance_fare) * traffic_multiplier * demand_multiplier * time_multiplier

    return {
        "base_fare": base_fare,
        "distance_fare": distance_fare,
        "traffic_multiplier": traffic_multiplier,
        "demand_multiplier": demand_multiplier,
        "time_multiplier": time_multiplier,
        "total_fare": round(total_fare, 2),
    }


def get_traffic_multiplier(traffic_level):
    """
    Returns the traffic multiplier based on the traffic level, using caching.
    """
    cache_key = f"traffic_multiplier_{traffic_level}"
    multiplier = cache.get(cache_key)

    if multiplier is None:
        traffic_multipliers = {
            "low": 1.0,
            "normal": 1.0,
            "high": 1.5,
        }
        multiplier = traffic_multipliers.get(traffic_level, 1.0)
        cache.set(cache_key, multiplier, timeout=60 * 5)  # Cache for 5 minutes

    return multiplier

def get_time_multiplier(current_time=None):
    """
    Returns the time multiplier based on the current time, using caching.
    """
    if current_time is None:
        current_time = datetime.datetime.now().time()

    cache_key = f"time_multiplier_{current_time.hour}"
    multiplier = cache.get(cache_key)

    if multiplier is None:
        hour = current_time.hour
        if 7 <= hour < 9 or 17 <= hour < 19:  # Morning and evening rush hours
            multiplier = 1.3
        else:
            multiplier = 1.0

        cache.set(cache_key, multiplier, timeout=60 * 15)  # Cache for 15 minutes

    return multiplier


DEMAND_REQUEST_WINDOW = 60  # seconds
DEMAND_THRESHOLD = 5  # requests within window

def calculate_realtime_surge(demand_level):
    """
    Calculates a surge multiplier based on recent demand levels and caching.
    Simulates real-time demand by tracking request counts.
    """
    cache_key = "recent_requests_count"
    request_count = cache.get(cache_key)
    if request_count is None:
        request_count = 0
        cache.set(cache_key, request_count, timeout=DEMAND_REQUEST_WINDOW) # Set initial count and timeout

    # Increase and cache demand levels
    request_count += 1
    cache.set(cache_key, request_count, timeout=DEMAND_REQUEST_WINDOW)

    if demand_level == "peak":
      surge_multiplier = 1.8
    else:
      surge_multiplier = 1.0
    #Real Time Surge
    if request_count > DEMAND_THRESHOLD:

      if surge_multiplier < 2.0: # cap surge
          surge_multiplier = min(2.0, surge_multiplier + (request_count - DEMAND_THRESHOLD) * 0.05) #Dynamic surge adjust
    return surge_multiplier
