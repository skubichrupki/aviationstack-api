import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
INPUT_HOURS = os.getenv("HOURS", "2").strip()

arr_iata = "WRO"
hours = int(INPUT_HOURS)

url = "http://api.aviationstack.com/v1/flights"
params = {
    'access_key': AVIATIONSTACK_API_KEY,
    'limit': 40,
    'arr_iata': arr_iata
}

now = datetime.now(timezone.utc)
window_end = now + timedelta(hours=hours)

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()
data = response.json()
flights = data.get("data", [])
header = f"Arrivals at {arr_iata} in next {hours}H\n\n"
flights_summary = []

for flight in flights:
    
    arrival_scheduled = (flight.get("arrival") or {}).get("scheduled", "N/A")
    arrival_dt = datetime.fromisoformat(arrival_scheduled)

    if now <= arrival_dt <= window_end:
        airline_name = (flight.get("airline") or {}).get("name", "N/A")
        flight_iata = (flight.get("flight") or {}).get("iata", "N/A")
        departure_airport = (flight.get("departure") or {}).get("airport", "N/A")
        arrival_time = arrival_dt.strftime("%H:%M")
        flights_summary.append(f"{airline_name} {flight_iata} - from: {departure_airport} - arrival: {arrival_time}")

flights_result = header + "\n\n".join(flights_summary) if flights_summary else "No flights found"

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
telegram_json = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": flights_result
}

requests.post(telegram_url, json=telegram_json, timeout=15)