# app/weather_service.py

import os
import json
from pprint import pprint

import requests
from dotenv import load_dotenv

from app import APP_ENV

load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
MY_ZIP = os.getenv("MY_ZIP", default="20057")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", default="US")

def human_friendly_temp(my_temperature_f):
    """Rounds a decimal fahrenheit temperature to the nearest whole degree, adds degree symbol"""
    degree_sign = u"\N{DEGREE SIGN}"
    return f"{round(my_temperature_f)} {degree_sign}F"

def get_hourly_forecasts(zip_code=MY_ZIP, country_code=COUNTRY_CODE):
    # see: https://openweathermap.org/current
    request_url = f"https://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&units=imperial&appid={OPEN_WEATHER_API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    #print(parsed_response.keys()) #> dict_keys(['cod', 'message', 'cnt', 'list', 'city'])
    result = {
        "city_name": parsed_response["city"]["name"],
        "hourly_forecasts": []
    }
    for forecast in parsed_response["list"][0:9]:
        #print(forecast.keys()) #> dict_keys(['dt', 'main', 'weather', 'clouds', 'wind', 'sys', 'dt_txt'])
        result["hourly_forecasts"].append({
            "timestamp": forecast["dt_txt"],
            "temp": human_friendly_temp(forecast["main"]["feels_like"]),
            "conditions": forecast["weather"][0]["description"]
        })
    return result

if __name__ == "__main__":

    if APP_ENV == "development":
        zip_code = input("PLEASE INPUT A ZIP CODE (e.g. 06510): ")
        results = get_hourly_forecasts(zip_code=zip_code) # invoke with custom params
    else:
        results = get_hourly_forecasts() # invoke with default params

    print("-----------------")
    print(f"TODAY'S WEATHER FORECAST FOR {results['city_name'].upper()}...")
    print("-----------------")

    for hourly in results["hourly_forecasts"]:
        print(hourly["timestamp"], "|", hourly["temp"], "|", hourly["conditions"])
