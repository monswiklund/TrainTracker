# main.py
import sys
import os

# Lägger till den nuvarande filens mapp till sys.path så att moduler i samma mapp kan importeras
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime, timedelta
from dateutil.parser import parse
from google_auth import authenticate_google  # Importera autentisering för Google API
from calendar_service import create_calendar_event, add_event_to_calendar  # Importera funktioner för Google Calendar
from vasttrafik_api import get_access_token, fetch_journeys  # Importera funktioner för Västtrafik API


# Huvudfunktion för programmet
def main():
    # Hämtar access token för Västtrafik API
    access_token = get_access_token()
    if not access_token:
        return  # Avbryter om ingen access token kunde hämtas

    # Autentiserar Google-kalendern en gång och erhåller autentiseringsuppgifter (creds)
    creds = authenticate_google()

    # Specifika tider (05:00) då programmet letar efter tåg
    specific_times = ['05:00']

    # Loopa genom de kommande 10 dagarna för att leta efter tåg
    for day_offset in range(10):
        # Beräknar datumet för den aktuella iterationen
        current_date = datetime.now() + timedelta(days=day_offset)

        # Kollar om dagen är en måndag (0) eller onsdag (2)
        if current_date.weekday() in [0, 2]:
            # Loopa genom alla specifika tider för att söka efter resor vid dessa tidpunkter
            for time_str in specific_times:
                # Konverterar tidsträngen till ett datetime-objekt
                current_time = datetime.strptime(time_str, "%H:%M")

                # Anropar Västtrafik API för att hämta tågdata för aktuell dag och tid
                data = fetch_journeys(access_token, current_date, current_time)

                # Kontrollera om det finns resultat
                if data and data["results"]:
                    print(f"Tåg hittade för {current_date.strftime('%Y-%m-%d')} kl {current_time.strftime('%H:%M')}:")

                    # Loopa genom varje resultat och skapa en kalenderhändelse för giltiga resor
                    for result in data["results"]:
                        # Hämtar planerade avgångs- och ankomsttider från resultatet
                        planned_departure = parse(result['tripLegs'][0]['plannedDepartureTime'])
                        planned_arrival = parse(result['tripLegs'][0]['plannedArrivalTime'])

                        # Kontrollera att avgången är mellan kl 05 och 07 och att ankomsten är senast kl 09
                        if 5 <= planned_departure.hour < 7 and planned_arrival.hour <= 9:
                            # Hämta startplats och destination
                            origin = result['tripLegs'][0].get('origin', {}).get('stopArea', {}).get('name',
                                                                                                     'Källby ->')
                            destination = result['tripLegs'][0].get('destination', {}).get('stopArea', {}).get('name',
                                                                                                               'Göteborg Central')

                            # Skapa en dictionary med information om resan
                            journey = {
                                'departure': planned_departure.isoformat(),
                                'arrival': planned_arrival.isoformat(),
                                'origin': origin,
                                'destination': destination
                            }

                            # Skapa en kalenderhändelse baserat på resans data
                            event = create_calendar_event(journey['departure'], journey['arrival'], journey['origin'],
                                                          journey['destination'])

                            # Lägg till kalenderhändelsen till Google Calendar
                            add_event_to_calendar(creds, event)
                else:
                    # Meddelande om inga tåg hittades för aktuell dag och tid
                    print(
                        f"Inga tåg hittades för {current_date.strftime('%Y-%m-%d')} kl {current_time.strftime('%H:%M')}.")