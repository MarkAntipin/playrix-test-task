from unittest.mock import MagicMock

from src.services.synchronize_data import SynchronizeDataService


def test_synchronize_data__data_is_outdated__updated_and_inserted(
    gridly_repo_outdated_data_mock: MagicMock, google_sheets_repo_mock: MagicMock
) -> None:
    # arrange
    service = SynchronizeDataService(
        google_sheets_client=MagicMock(),
        gridly_client=MagicMock(),
        spreadsheet_id='1',
        db_id='1',
    )
    service.google_sheets_repo = google_sheets_repo_mock
    service.gridly_repo = gridly_repo_outdated_data_mock

    # act
    service.synchronize_from_google_sheets_to_gridly(
        grid_name='1',
        worksheet_name='1',
    )

    # assert
    assert gridly_repo_outdated_data_mock.update_records.called
    assert gridly_repo_outdated_data_mock.add_records.called


def test_synchronize_data__data_is_already_synchronized__no_insertion(
    gridly_repo_actual_data_mock: MagicMock, google_sheets_repo_mock: MagicMock
) -> None:
    # arrange
    service = SynchronizeDataService(
        google_sheets_client=MagicMock(),
        gridly_client=MagicMock(),
        spreadsheet_id='1',
        db_id='1',
    )
    service.google_sheets_repo = google_sheets_repo_mock
    service.gridly_repo = gridly_repo_actual_data_mock

    # act
    service.synchronize_from_google_sheets_to_gridly(
        grid_name='1',
        worksheet_name='1',
    )

    # assert
    assert not gridly_repo_actual_data_mock.update_records.called
    assert not gridly_repo_actual_data_mock.add_records.called
