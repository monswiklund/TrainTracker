# google_auth.py
from google.oauth2.credentials import Credentials  # Importerar Credentials-klass för autentisering
from google_auth_oauthlib.flow import InstalledAppFlow  # Importerar flow-klass för att hantera OAuth2-flödet
from google.auth.transport.requests import Request  # Request-klass för att förnya autentiseringstoken
import os.path  # Importerar os.path för att hantera filsystemet

# Definierar de behörigheter som krävs (scope) för Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']


# Funktion för att autentisera och erhålla autentiseringsuppgifter för Google API
def authenticate_google():
    creds = None  # Initialiserar creds-variabeln som None

    # Kontrollera om det redan finns en token-fil med giltiga autentiseringsuppgifter
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Om det inte finns några giltiga autentiseringsuppgifter, skaffa nya
    if not creds or not creds.valid:
        # Om token har gått ut men det finns en refresh token, förnya token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Starta ett nytt autentiseringsflöde och be om användarbehörighet
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Spara de nya autentiseringsuppgifterna i en fil för framtida användning
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Returnera autentiseringsuppgifterna
    return creds