# calendar_service.py
from googleapiclient.discovery import build  # Importera Google API-klienten för att interagera med Google Calendar


# Funktion för att skapa ett kalenderhändelseobjekt för en tågresa
def create_calendar_event(departure, arrival, origin, destination):
    # Skapa en händelse med information om resa, avgång och destination
    event = {
        'summary': f'Train from {origin} to {destination}',  # Sammanfattning (titel) på händelsen
        'location': destination,  # Destination (plats för händelsen)
        'description': 'Train journey',  # Beskrivning av händelsen
        'start': {  # Starttid för händelsen
            'dateTime': departure,  # Avgångstid
            'timeZone': 'Europe/Stockholm',  # Tidszon
        },
        'end': {  # Sluttid för händelsen
            'dateTime': arrival,  # Ankomsttid
            'timeZone': 'Europe/Stockholm',  # Tidszon
        },
    }
    return event  # Returnera det skapade händelseobjektet


# Funktion för att lägga till en händelse i Google Calendar
def add_event_to_calendar(creds, event):
    # Skapa en tjänstanslutning till Google Calendar API med hjälp av autentiseringsuppgifter
    service = build('calendar', 'v3', credentials=creds)

    # Anropa API:et för att infoga (lägga till) händelsen i primära kalendern
    event_result = service.events().insert(calendarId='primary', body=event).execute()

    # Visa en bekräftelse med en länk till den skapade händelsen i Google Calendar
    print(f"Event created: {event_result.get('htmlLink')}")