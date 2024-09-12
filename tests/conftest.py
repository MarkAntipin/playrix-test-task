import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'


def _load_json(file_path: Path) -> dict:
    with file_path.open() as f:
        return json.load(f)


@pytest.fixture
def google_sheets_repo_mock() -> MagicMock:
    repo = MagicMock()
    repo.get_records.return_value = _load_json(_TEST_DATA_DIR / 'get_google_sheets_records.json')
    return repo


@pytest.fixture
def gridly_repo_actual_data_mock() -> MagicMock:
    repo = MagicMock()
    repo.get_grid.return_value = _load_json(_TEST_DATA_DIR / 'get_grid.json')
    repo.get_records_by_id.return_value = _load_json(_TEST_DATA_DIR / 'get_gridly_records_actual.json')
    repo.get_column_names_mapping.return_value = _load_json(_TEST_DATA_DIR / 'get_column_names_mapping.json')
    return repo


@pytest.fixture
def gridly_repo_outdated_data_mock() -> MagicMock:
    repo = MagicMock()
    repo.get_grid.return_value = _load_json(_TEST_DATA_DIR / 'get_grid.json')
    repo.get_records_by_id.return_value = _load_json(_TEST_DATA_DIR / 'get_gridly_records_outdated.json')
    repo.get_column_names_mapping.return_value = _load_json(_TEST_DATA_DIR / 'get_column_names_mapping.json')
    return repo
