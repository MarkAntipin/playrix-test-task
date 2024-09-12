import logging
import typing as tp

from src.utils.gridly.get_client import GridlyApi
from src.utils.http import HttpMethods

logger = logging.getLogger(__name__)


class GridlyRepo:
    def __init__(self, client: GridlyApi, db_id: str) -> None:
        self.client = client
        self.db_id = db_id

    def get_grid(self, grid_name: str) -> dict | None:
        grids = self._get_grids()
        if not grids:
            return
        for grid in grids:
            if grid['name'] == grid_name:
                return grid

    def get_records_by_id(self, view_id: str) -> dict[str, tp.Any] | None:
        records = self._get_records(view_id=view_id)
        if not records:
            logger.error(f'Error getting records by view id: {view_id}')
            return

        return {record['id']: record for record in records}

    def get_column_names_mapping(self, grid_id: str) -> dict[str, str] | None:
        grid = self._get_grid(grid_id=grid_id)
        if not grid:
            logger.error(f'Error getting grid by id: {grid_id}')
            return

        return {column['id']: column['name'] for column in grid['columns']}

    def add_records(self, view_id: str, records: list[dict]) -> dict | None:
        r = self.client.make_request(
            uri=f'v1/views/{view_id}/records',
            method=HttpMethods.POST,
            data=records,
        )
        return r

    def update_records(self, view_id: str, records: list[dict]) -> dict | None:
        r = self.client.make_request(
            uri=f'v1/views/{view_id}/records',
            method=HttpMethods.PATCH,
            data=records,
        )
        return r

    def _get_grids(self) -> dict | None:
        r = self.client.make_request(
            uri='v1/grids',
            method=HttpMethods.GET,
            params={
                'dbId': self.db_id
            }
        )
        return r

    def _get_grid(self, grid_id: str) -> dict | None:
        r = self.client.make_request(
            uri=f'v1/grids/{grid_id}',
            method=HttpMethods.GET,
        )
        return r

    def _get_records(self, view_id: str) -> dict | None:
        r = self.client.make_request(
            uri=f'v1/views/{view_id}/records',
            method=HttpMethods.GET,
        )
        return r
