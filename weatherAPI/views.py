from http.client import BAD_REQUEST
from django.shortcuts import render,redirect
from urllib.request import urlopen
import json
from datetime import datetime as dt
from pytz import timezone
from urllib.error import URLError, HTTPError
# Create your views here.
def WeatherCheckView(request):

    # Fetching data from openweather site
    url = 'https://api.openweathermap.org/data/2.5/weather?q='
    apiKey = '6d4ad160fe4f3b48806166fba0ec988e'

    # Using ip finder site
    IP_Finder_Source = urlopen("http://ipinfo.io/json").read()

    # Show the weather by user location
    IP_Finder = json.loads(IP_Finder_Source)
    
    try:

        if request.method == "POST":
            city = request.POST.get('city',IP_Finder['city'])
    
            if city.isdigit():
                city = IP_Finder['city']
            data = urlopen(url+city+"&appid="+apiKey).read()
            data = json.loads(data)
            # Current day
            today = dt.now().strftime("%A")

            country = data['sys']['country']

            context = {

            "today":today,

            "country":country,
            "city":city,

            # converting to celsius
            "temperature":int(data['main']['temp']-273.15),

            # Coordinate point
            "coordinate":data['coord'],
            
            "main":data['main'],
            "weather":data['weather'],

            }
        else:
            # First we save timezone then take the data and time
            time_zone = timezone(IP_Finder['timezone'])

            # Current day
            today = dt.now().strftime("%A")

            #Current date
            date = dt.now().strftime("%B %d, %Y")

            # Showing time based on user timezone
            DateTime = dt.now(time_zone).strftime('%H:%M:%S')

            # Getting city and country by IP.
            city = IP_Finder['city']
            country = IP_Finder['country']

            data = urlopen(url+city+"&appid="+apiKey).read()

            # Convert the source code to json
            data = json.loads(data)

            context = {

                "today":today,

                "current_date":date,

                "DateTime":DateTime ,


                "country":country,
                "city":city,

                # converting to celsius
                "temperature":int(data['main']['temp']-273.15),

                # Coordinate point
                "coordinate":data['coord'],
                
                "main":data['main'],
                "weather":data['weather'],

            }
        return render(request,'weatherAPI/weather.html',context)
    except HTTPError as e:
        if e.code == 404:
            return redirect('weather_api:handler404')
    
def Handler404(request):
    return render(request,'weatherAPI/handler404.html',context={})
