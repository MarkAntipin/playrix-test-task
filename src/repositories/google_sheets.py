import logging

import gspread

logger = logging.getLogger(__name__)


class GoogleSheetsRepo:
    def __init__(self, client: gspread.Client, spreadsheet_id: str) -> None:
        self.client = client
        self.spreadsheet_id = spreadsheet_id

    def get_records(self, worksheet_name: str) -> list[dict] | None:
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        except gspread.exceptions.SpreadsheetNotFound as e:
            logger.error(f'Error opening spreadsheet by key: {e}')
            return

        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound as e:
            logger.error(f'Error opening worksheet by name: {e}')
            return

        return worksheet.get_all_records()
