from django.http import HttpResponse
import requests
import json

# This code can be in an other place i.e. settings.py

HOST = 'http://127.0.0.1:5000/'
ACCUWEATHER = HOST + 'accuweather?latitude={}&longitude={}'
NOAA = HOST + 'noaa?latlon={},{}'
WEATHERDOTCOM = HOST + 'weatherdotcom'


def call_accuweather_fahrenheit(latitude, longitude):
    req_accuweather = requests.get(ACCUWEATHER.format(latitude, longitude))
    return float(json.loads(req_accuweather.text)['simpleforecast']['forecastday'][0]['current']['fahrenheit'])

def call_noaa_fahrenheit(latitude, longitude):
    req_noaa = requests.get(NOAA.format(latitude, longitude))
    return float(json.loads(req_noaa.text)['today']['current']['fahrenheit'])

def call_weatherdotcom_fahrenheit(longitude, latitude):
    req_weatherdotcom = requests.post(WEATHERDOTCOM, json={'lat': latitude, 'lon': longitude})
    return float(json.loads(req_weatherdotcom.text)['query']['results']['channel']['condition']['temp'])

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32)*5/9

# This code can be in an other place i.e. settings.py


def average_temperature(request):

    SERVERS_AVAILABLE = {
        'accuweather': call_accuweather_fahrenheit,
        'noaa': call_noaa_fahrenheit,
        'weatherdotcom': call_weatherdotcom_fahrenheit,
    }

    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    search_filter = request.GET.get('filter', None)

    if latitude == None or longitude == None or search_filter == None:
        return HttpResponse(json.dumps({'error': 'errors in params'}))

    search_filter = search_filter.split('_')
    count = 0
    fahrenheit_average = 0

    for server in search_filter:
        if not(server.lower() in SERVERS_AVAILABLE):
            return HttpResponse(json.dumps({'error': 'there are invalid hosts'}))
        elif search_filter.count(server.lower()) > 1:
            return HttpResponse(json.dumps({'error': 'a server name is duplicated'}))
        else:
            try:
                fahrenheit_average += SERVERS_AVAILABLE[server.lower()](latitude, longitude)
                count += 1
            except:
                return HttpResponse(json.dumps({'error': 'there are problems with some apis'}))
    
    fahrenheit_average /= count

    return HttpResponse(json.dumps({'fahrenheit_average': round(fahrenheit_average,1), 'celsius_average': round(fahrenheit_to_celsius(fahrenheit_average),1)}))