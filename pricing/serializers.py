from rest_framework import serializers

        
class FareCalculationSerializer(serializers.Serializer):
    distance = serializers.FloatField(required=True, min_value=0)
    traffic_level = serializers.ChoiceField(choices=['low', 'normal', 'high'], default='normal')
    demand_level = serializers.ChoiceField(choices=['low', 'normal', 'high', 'peak'], default='normal')
    

class FareResponseSerializer(serializers.Serializer):
    base_fare = serializers.DecimalField(max_digits=6, decimal_places=2)
    distance_fare = serializers.DecimalField(max_digits=8, decimal_places=2)
    traffic_multiplier = serializers.DecimalField(max_digits=4, decimal_places=2)
    demand_multiplier = serializers.DecimalField(max_digits=4, decimal_places=2)
    time_multiplier = serializers.DecimalField(max_digits=4, decimal_places=2)
    total_fare = serializers.DecimalField(max_digits=10, decimal_places=2)
