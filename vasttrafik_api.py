# vasttrafik_api.py
import requests
import base64
from config import CLIENT_ID, CLIENT_SECRET  # Importera API-nycklar från config.py
from datetime import datetime, timedelta
from dateutil.parser import parse


# Funktion för att hämta ett access token från Västtrafik API
def get_access_token():
    # Kombinera klient-ID och klient-hemlighet till en autentiseringssträng
    auth_key = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_key_encoded = base64.b64encode(auth_key.encode()).decode()  # Base64-koda strängen
    token_url = "https://ext-api.vasttrafik.se/token"  # API-endpoint för att hämta token

    # Header för tokenförfrågan med Basic Authentication
    token_headers = {
        "Authorization": f"Basic {auth_key_encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data som skickas i tokenförfrågan
    token_data = {
        "grant_type": "client_credentials"
    }

    # Skicka en POST-förfrågan för att hämta access token
    token_response = requests.post(token_url, headers=token_headers, data=token_data)

    # Kontrollera om förfrågan lyckades
    if token_response.status_code == 200:
        # Returnera access token om förfrågan var framgångsrik
        return token_response.json().get("access_token")
    else:
        # Hantera fel och visa svarskod och felmeddelande
        print(f"Error fetching access token: {token_response.status_code}")
        print("Response text:", token_response.text)
        return None


# Funktion för att hämta tågresa-data från Västtrafik API
def fetch_journeys(access_token, current_date, current_time):
    url = "https://ext-api.vasttrafik.se/pr/v4/journeys"  # API-endpoint för att hämta resedata

    # Parametrar för API-förfrågan, inkluderar start- och slutplats samt datum och tid
    params = {
        "originGid": "9021014034001000",  # ID för startplats (Källby)
        "originLatitude": 58.51031,
        "originLongitude": 13.30191,
        "destinationGid": "9021014008000000",  # ID för slutdestination (Göteborg Central)
        "destinationLatitude": 57.70893,
        "destinationLongitude": 11.97291,
        "dateTime": current_date.replace(hour=current_time.hour, minute=current_time.minute).strftime(
            '%Y-%m-%dT%H:%M:%S%z'),  # Datum och tid för avgång
        "dateTimeRelatesTo": "departure",  # Ange att tidsangivelsen är för avgång
        "limit": 7,  # Max antal resor att returnera
        "transportModes": "train",  # Begränsa till resor med tåg
        "onlyDirectConnections": "true",  # Endast direkta resor, inga byten
        "includeNearbyStopAreas": "false"  # Inkludera inte närliggande hållplatser
    }

    # Header för förfrågan, använder Bearer-token för autentisering
    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }

    # Skicka GET-förfrågan med headers och parametrar
    response = requests.get(url, headers=headers, params=params)

    # Kontrollera om förfrågan lyckades
    if response.status_code == 200:
        # Returnera resedata om förfrågan var framgångsrik
        return response.json()
    else:
        # Hantera fel och visa svarskod och felmeddelande
        print(f"Error fetching data: {response.status_code}")
        print("Response text:", response.text)
        return None