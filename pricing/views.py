from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ride_hailing import settings
from .serializers import FareCalculationSerializer, FareResponseSerializer
from .services import PricingService
import asyncio
import logging

logger = logging.getLogger(__name__)

class CalculateFareView(APIView):
    def get(self, request):
        try:
            serializer = FareCalculationSerializer(data=request.query_params)
            if not serializer.is_valid():
                logger.warning(f"Invalid request parameters: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            distance = serializer.validated_data['distance']
            traffic_level = serializer.validated_data['traffic_level']
            demand_level = serializer.validated_data['demand_level']

            cache_key = f"fare:{distance}:{traffic_level}:{demand_level}"

            # 1. Check Cache
            cached_result = settings.CACHE.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for key: {cache_key}")
                return Response(cached_result, status=status.HTTP_200_OK)

            pricing_service = PricingService()
            try:
                fare_details = asyncio.run(self.calculate_fare_async(pricing_service, distance, traffic_level, demand_level))
            except Exception as e:
                logger.exception("Error during fare calculation in thread pool")
                return Response({'error': 'Fare calculation failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response_serializer = FareResponseSerializer(fare_details)
            serialized_data = response_serializer.data

            settings.CACHE.setdefault(cache_key, serialized_data)
            logger.info(f"Fare calculated and cached for key: {cache_key}")

            return Response(serialized_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Unexpected error in calculate_fare_view")
            return Response({'error': 'An unexpected error occurred.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def calculate_fare_async(self, pricing_service, distance, traffic_level, demand_level):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            settings.THREAD_POOL_EXECUTOR,
            pricing_service.calculate_fare,
            distance,
            traffic_level,
            demand_level
        )