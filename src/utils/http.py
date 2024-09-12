import logging
import typing as tp
from enum import StrEnum, auto

import requests

logger = logging.getLogger(__name__)


class HttpMethods(StrEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class BaseHttpApi:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.strip('/')
        self.api_key = api_key

    def make_request(
        self,
        uri: str,
        method: HttpMethods,
        data: tp.Any | None = None,
        params: dict | None = None,
    ) -> dict | None:
        uri = uri.strip('/')
        full_url = f'{self.base_url}/{uri}'

        logger.info(f'Making {method} request to {full_url}')
        r = requests.request(
            method=method,
            url=full_url,
            headers={'Authorization': f'ApiKey {self.api_key}'},
            json=data,
            params=params
        )
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f'Error making request: {e}', exc_info=True)
            return None

        return r.json()
