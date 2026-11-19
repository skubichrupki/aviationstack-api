import requests
import os
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(AVIATIONSTACK_API_KEY)

url = "http://api.aviationstack.com/v1/flights"
params = {
    'access_key': AVIATIONSTACK_API_KEY,
    'limit': 5,
    'dep_iata': "WRO"
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()
data = response.json()

flights = data.get("data", [])
flights_summary = []

for flight in flights:
    airline_name = (flight.get("airline") or {}).get("name", "N/A")
    flight_iata = (flight.get("flight") or {}).get("iata", "N/A")
    departure_airport = (flight.get("departure") or {}).get("airport", "N/A")
    arrival_airport = (flight.get("arrival") or {}).get("airport", "N/A")
    arrival_scheduled = (flight.get("arrival") or {}).get("scheduled", "N/A")
    flights_summary.append(f"{airline_name} {flight_iata} - from: {departure_airport} - to: {arrival_airport} - landing time:{arrival_scheduled}")

flights_result = "\n".join(flights_summary) or "No flights found"

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
telegram_json = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": flights_result
}

requests.post(telegram_url, json=telegram_json, timeout=15)