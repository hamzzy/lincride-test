# pricing_api/pricing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('calculate-fare/', views.CalculateFareView.as_view(), name='calculate-fare'),
]