# Note! For the code to work you need to replace all the placeholders with
# Your own details. e.g. account_sid, lat/lon, from/to phone numbers.

import os
from os.path import dirname
from os.path import join
import requests
from dotenv import find_dotenv
from dotenv import load_dotenv
from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client

load_dotenv(find_dotenv())
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
LAT = -23.534640
LNG = -46.423770
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
API_KEY = os.environ.get("OWM_API_KEY")

weather_params = {
    "lat": LAT,
    "lon": LNG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
            body="It's going to rain today. Remember to bring an ☔️",
            from_="YOUR TWILIO VIRTUAL NUMBER",
            to="YOUR TWILIO VERIFIED REAL NUMBER"
        )
    print(message.status)
