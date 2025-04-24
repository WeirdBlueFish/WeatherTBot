import requests
from base import *
import pytz
import requests
from datetime import datetime, timedelta

def get_city(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

def forecast(city):
    URL = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(URL)
    return response.json()

def get_rain(response):
    if response['list']:
        single_forecast = response['list'][0]  
        pop = single_forecast.get('pop', 0)
        return pop * 100
    else:
        return None

def get_degrees(response):
    return (response['main']['temp'])

def get_description(response):
    return (response['weather'][0]['description'])

def get_humidity(response):
    return (response['main']['humidity'])

def get_country(response):
    return (response['sys']['country'])

def get_name(response):
    return (response['name'])

def get_timezone(response):
    return (response['timezone'])

def get_visibility(response):
    return (response['visibility'])

def get_weather_main(response):
    return (response['weather'][0]['main'])

def get_weather_description(response):
    return (response['weather'][0]['description'])

def get_weather_icon(response):
    return (response['weather'][0]['icon'])

def get_feels_like(response):
    return (response['main']['feels_like'])

def get_temp_min(response):
    return (response['main']['temp_min'])

def get_temp_max(response):
    return (response['main']['temp_max'])

def get_pressure(response):
    return (response['main']['pressure'])

def get_humidity(response):
    return (response['main']['humidity'])

def get_visibility(response):
    return (response['visibility'])

def get_wind_speed(response):
    return (response['wind']['speed'])

def get_wind_deg(response):
    return (response['wind']['deg'])

def get_sunrise(response):
    return (response['sys']['sunrise'])

def get_sunset(response):
    return (response['sys']['sunset'])

def get_lon(response):
    return (response['coord']['lon'])

def get_lat(response):
    return (response['coord']['lat'])

def current_time(city):
    utc_now = datetime.utcnow()

    timezone_offset = get_timezone(city) 

    local_time = utc_now + timedelta(seconds=timezone_offset)
    return local_time.strftime('%H:%M:%S')

def LatLon(city):
    LAT = get_lat(city)
    LON = get_lon(city)
   
    URL = f'https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}&formatted=0'
    response = requests.get(URL)
    data = response.json()

    sunrise_utc = data['results']['sunrise']
    sunset_utc = data['results']['sunset']
    return sunrise_utc, sunset_utc

def convert_utc_to_local(utc_time):
    utc_time = datetime.fromisoformat(utc_time)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tehran'))
    return local_time.strftime('%H:%M:%S')

def sunrise(city):
    sunrise_utc, sunset_utc = LatLon(city)
    sunrise_local = convert_utc_to_local(sunrise_utc)
    return sunrise_local

def sunset(city):
    sunrise_utc, sunset_utc = LatLon(city)
    sunset_local = convert_utc_to_local(sunset_utc)
    return sunset_local

def show_all(response):
    if response['cod'] == '404':
        return 'City not found!'
    if response['cod'] == '400':
        return 'Please enter a city name!'
    if response['cod'] == '429':
        return 'Too many requests!'
    else:
        return f"City: {get_name(response)}\
                \nCountry: {get_country(response)}\
                \nTemperature: {get_degrees(response)} ℃\
                \nWeather: {get_weather_main(response)}\
                \nRain Possibility: {get_rain(forecast(get_name(response)))} ٪\
                \nDescription: {get_weather_description(response)}\
                \nWind speed: {get_wind_speed(response)} m/s\
                \nWind degrees: {get_wind_deg(response)}°\
                \nHumidity: {get_humidity(response)} ٪\
                \nPressure: {get_pressure(response)} mbar\
                \nVisibility: {get_visibility(response)}\
                \nReal Feel: {get_feels_like(response)} ℃\
                \nMin temperature: {get_temp_min(response)} ℃\
                \nMax temperature: {get_temp_max(response)} ℃\
                \nSunrise: {sunrise(response)}\
                \nSunset: {sunset(response)}\
                \nCurrent Time: {current_time(response)}"