import gspread
from google.oauth2.service_account import Credentials

from settings import GoogleSheetsSettings


def get_google_sheets_client(google_sheets_settings: GoogleSheetsSettings) -> gspread.Client:
    creds = Credentials.from_service_account_file(
        filename=google_sheets_settings.TOKEN_FILE_NAME,
        scopes=google_sheets_settings.SCOPES
    )
    client = gspread.authorize(creds)
    return client
