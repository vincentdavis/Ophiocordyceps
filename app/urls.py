from django.contrib import admin
from django.urls import path, include
from . import views
from PowerMeterTx import PowerMeterTx
from config import DEBUG, LOG, NETKEY, POWER_SENSOR_ID

urlpatterns = [
    path('', views.LandingView.as_view(), name="home_page"),  # Login Root url
    path('request', views.Request.as_view(), name="Request"),  # Login Root url

]