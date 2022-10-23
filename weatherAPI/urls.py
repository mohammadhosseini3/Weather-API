from django.urls import path
from . import views

app_name = "weather_api"
urlpatterns = [
    path("",views.WeatherCheckView,name="WeatherCheck"),
    path("404/",views.Handler404,name="handler404"),
]