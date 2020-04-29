# app/daily_briefing.py

import os
from dotenv import load_dotenv
from datetime import date
#from pprint import pprint

from app import APP_ENV
from app.weather_service import get_hourly_forecasts
from app.email_service import send_email

load_dotenv()

MY_NAME = os.getenv("MY_NAME", default="Player 1")

if __name__ == "__main__":

    if APP_ENV == "development":
        zip_code = input("PLEASE INPUT A ZIP CODE (e.g. 06510): ")
        weather_results = get_hourly_forecasts(zip_code=zip_code) # invoke with custom params
    else:
        weather_results = get_hourly_forecasts() # invoke with default params

    #print(weather_results)

    html = ""
    html += f"<h3>Good Morning, {MY_NAME}!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{date.today().strftime('%A, %B %d, %Y')}</p>"

    html += f"<h4>Weather Forecast for {weather_results['city_name'].title()}</h4>"
    html += "<ul>"
    for hourly in weather_results["hourly_forecasts"]:
        html += f"<li>{hourly['timestamp']} | {hourly['temp']} | {hourly['conditions'].upper()}</li>"
    html += "</ul>"

    send_email(subject="[Daily Briefing] My Morning Report", html=html)
