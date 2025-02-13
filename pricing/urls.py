# pricing_api/pricing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('calculate-fare/', views.calculate_fare_api, name='calculate_fare'),
]