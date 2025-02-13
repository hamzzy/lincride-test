from rest_framework.decorators import api_view
from rest_framework.response import Response
from .pricing_logic import calculate_fare
import datetime

@api_view(['GET'])
def calculate_fare_api(request):
    """
    API endpoint to calculate the ride fare based on dynamic pricing.
    """
    distance = float(request.query_params.get('distance', 0))
    traffic_level = request.query_params.get('traffic_level', 'normal')
    demand_level = request.query_params.get('demand_level', 'normal')
    current_time_str = request.query_params.get('current_time')

    try:
        # Optionally handle time input as a parameter
        if current_time_str:
            try:
                 current_time = datetime.datetime.strptime(current_time_str, '%H:%M').time()
            except ValueError:
                return Response({'error': 'Invalid time format. Use HH:MM'}, status=400)
        else:
            current_time = datetime.datetime.now().time()

        fare_details = calculate_fare(distance, traffic_level, demand_level, current_time)
        return Response(fare_details)
    except ValueError as e:
        return Response({'error': str(e)}, status=400)