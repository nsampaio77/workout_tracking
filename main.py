import os
import requests
import datetime as dt
from math import floor

APP_ID = os.environ.get("APP_NUTRITIONIX")
API_KEY = os.environ.get("API_KEY_NUTRITIONIX")
PUBLIC_KEY = os.environ.get("API_PUBLIC_KEY_SHEETY")
BEARER_TOKEN_SHEET = os.environ.get("BEARER_TOKEN_SHEET")
NUTRITION_ENDPOINT = "https://trackapi.nutritionix.com"
NATURAL_EXERCISE_RESOURCE = "v2/natural/exercise"
SHEETY_ENDPOINT = f"https://api.sheety.co/{PUBLIC_KEY}/myWorkouts/page1"


headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

sheety_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN_SHEET}"
}
query_str = input("What have you done?")
parameters_req = {"query": query_str}
response = requests.post(url=f"{NUTRITION_ENDPOINT}/{NATURAL_EXERCISE_RESOURCE}", json=parameters_req, headers=headers)
result = response.json()

# Google Sheet
today_date = dt.datetime.now().strftime("%d/%m/%Y")
now_time = dt.datetime.now().strftime("%X")

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
    sheet_response = requests.post(url=SHEETY_ENDPOINT, json=data, headers=sheety_headers)
    if str(sheet_response.status_code) == "200":
        print("Data sent successfully")
