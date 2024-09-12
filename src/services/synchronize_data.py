import logging

import gspread

from src.repositories.google_sheets import GoogleSheetsRepo
from src.repositories.gridly import GridlyRepo
from src.utils.gridly.get_client import GridlyApi
from src.utils.mappers import from_google_sheets_to_gridly, from_gridly_to_google_sheets

logger = logging.getLogger(__name__)


class SynchronizeDataService:
    def __init__(
        self,
        google_sheets_client: gspread.Client,
        gridly_client: GridlyApi,
        spreadsheet_id: str,
        db_id: str,
    ) -> None:
        self.google_sheets_repo = GoogleSheetsRepo(
            client=google_sheets_client,
            spreadsheet_id=spreadsheet_id
        )
        self.gridly_repo = GridlyRepo(
            client=gridly_client,
            db_id=db_id
        )

    def synchronize_from_google_sheets_to_gridly(
        self,
        grid_name: str,
        worksheet_name: str,
        id_column_name: str = 'Record ID',
        version_column_name: str = 'Version',
    ) -> None:
        google_sheets_records = self.google_sheets_repo.get_records(worksheet_name=worksheet_name)
        if not google_sheets_records:
            logger.error('Error getting google sheets records')
            return

        grid = self.gridly_repo.get_grid(grid_name=grid_name)
        if not grid:
            logger.error('Error getting grid')
            return

        view_id = grid['defaultAccessViewId']
        gridly_records_by_id = self.gridly_repo.get_records_by_id(view_id=view_id)
        column_names_mapping = self.gridly_repo.get_column_names_mapping(grid_id=grid['id'])
        reversed_column_names_mapping = {v: k for k, v in column_names_mapping.items()}

        records_to_insert = []
        records_to_update = []
        for google_sheets_record in google_sheets_records:
            gridly_record = gridly_records_by_id.get(google_sheets_record[id_column_name])
            google_sheets_record_gridly_format = from_google_sheets_to_gridly(
                google_sheets_record=google_sheets_record,
                column_names_mapping=reversed_column_names_mapping,
                id_column_name=id_column_name,
            )

            if not gridly_record:
                records_to_insert.append(google_sheets_record_gridly_format)
                continue

            gridly_record_google_sheets_format = from_gridly_to_google_sheets(
                gridly_record=gridly_record,
                column_names_mapping=column_names_mapping,
            )

            if (
                int(gridly_record_google_sheets_format[version_column_name])
                < int(google_sheets_record[version_column_name])
            ):
                records_to_update.append(google_sheets_record_gridly_format)

        if records_to_insert:
            r = self.gridly_repo.add_records(view_id=view_id, records=records_to_insert)
            if r is None:
                logger.error('Error adding records')
            else:
                logger.info(f'Inserted {len(records_to_insert)} new records')

        else:
            logger.info('No records to insert')

        if records_to_update:
            r = self.gridly_repo.update_records(view_id=view_id, records=records_to_update)
            if r is None:
                logger.error('Error updating records')
            else:
                logger.info(f'Updated {len(records_to_update)} records')
        else:
            logger.info('No records to update')
