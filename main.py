import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoints = "https://home.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_Key")

# proxy_client = TwilioHttpClient()
# proxy_client.session.proxies =  {'https': os.environ['http_proxy']}

account_sid = "AC7c357bb2c70d78979800071781270f39"
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": 27.2046,
    "lon": 77.4977,
    "appid": api_key,
    "exclude": "current ,minutely, daily"
}

response = requests.get(OWM_Endpoints, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['http_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It May Rain Please Be Aware....",
        from_="+918898084899",
        to="+916678045688"
    )

    print(message.status)

# print(weather_data["hourly"][0]["weather"][0]["id"])
