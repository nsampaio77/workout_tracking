"""


Resources:
 SHeety - https://sheety.co/

"""

import os
import requests
import datetime as dt
from math import floor

app_id = os.environ.get("APP_NUTRITIONIX")
api_key = os.environ.get("API_KEY_NUTRITIONIX")
public_key = os.environ.get("API_PUBLIC_KEY_SHEETY")
NUTRITION_ENDPOINT = "https://trackapi.nutritionix.com"
NATURAL_EXERCISE_RESOURCE = "v2/natural/exercise"
sheety_endpoint = f"https://api.sheety.co/{public_key}/myWorkouts/page1"


headers = {
    "x-app-id": app_id,
    "x-app-key": api_key
}
query_str = input("What have you done?")
parameters_req = {"query": query_str}
response = requests.post(url=f"{NUTRITION_ENDPOINT}/{NATURAL_EXERCISE_RESOURCE}", json=parameters_req, headers=headers)
result = response.json()

# Google Sheet
today_date = dt.datetime.now().strftime("%d/%m/%Y")
now_time = dt.datetime.now().strftime("%X")
rows = []
for exe in result["exercises"]:
    hour = floor(float(exe['duration_min'] / 60))
    minutes = floor(float(exe['duration_min'] % 60))
    data = {
        "page1": {
            "date": today_date,
            "time": now_time,
            "exercise": exe['name'],
            "duration": f"{hour}h:{minutes}m"
        }
    }
    sheet_response = requests.post(url=sheety_endpoint, json=data)
    print(sheet_response)




