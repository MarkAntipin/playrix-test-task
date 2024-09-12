import logging

from settings import AppSettings, GoogleSheetsSettings, GridlySettings
from src.services.synchronize_data import SynchronizeDataService
from src.utils.google_sheets.get_client import get_google_sheets_client
from src.utils.gridly.get_client import get_gridly_client
from src.utils.setup_logger import setup_logger

logger = logging.getLogger(__name__)


class App:
    def __init__(self, service: SynchronizeDataService, app_settings: AppSettings) -> None:
        self.service = service
        self.app_settings = app_settings

    def run(self) -> None:

        for table_name in self.app_settings.TABLE_NAMES:
            logger.info(f'Starting synchronization for table: {table_name}')
            self.service.synchronize_from_google_sheets_to_gridly(
                grid_name=table_name,
                worksheet_name=table_name,
            )
            logger.info(f'Finished synchronization for table: {table_name}')


def create_app() -> App:
    setup_logger(level=logging.INFO)

    gridly_settings = GridlySettings()
    google_sheets_settings = GoogleSheetsSettings()
    app_settings = AppSettings()

    gridly_client = get_gridly_client(gridly_settings=gridly_settings)
    google_sheets_client = get_google_sheets_client(google_sheets_settings=google_sheets_settings)

    service = SynchronizeDataService(
        google_sheets_client=google_sheets_client,
        gridly_client=gridly_client,
        spreadsheet_id=google_sheets_settings.SPREADSHEET_ID,
        db_id=gridly_settings.DB_ID
    )

    return App(service=service, app_settings=app_settings)
