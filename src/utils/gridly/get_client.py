from settings import GridlySettings
from src.utils.http import BaseHttpApi


class GridlyApi(BaseHttpApi):
    pass


def get_gridly_client(gridly_settings: GridlySettings) -> GridlyApi:
    client = GridlyApi(
        base_url=gridly_settings.BASE_URL,
        api_key=gridly_settings.API_KEY,
    )
    return client
