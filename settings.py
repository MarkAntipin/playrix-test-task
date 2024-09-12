from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)


class GoogleSheetsSettings(BaseSettings):
    SPREADSHEET_ID: str
    TOKEN_FILE_NAME: str = 'token.json'
    SCOPES: list[str] = ['https://www.googleapis.com/auth/spreadsheets']

    class Config:
        case_sensitive = False
        env_prefix = "GOOGLE_SHEETS_"


class GridlySettings(BaseSettings):
    API_KEY: str
    DB_ID: str
    BASE_URL: str = 'https://api.gridly.com'

    class Config:
        case_sensitive = False
        env_prefix = "GRIDLY_"


class AppSettings(BaseSettings):
    TABLE_NAMES: list[str] = ['Static Texts', 'Game Text']
