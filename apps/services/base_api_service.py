import logging
from abc import ABC

import requests


class RequestService(ABC):
    logger: logging.Logger = logging.getLogger('django')

    @classmethod
    def get(
        cls,
        url: str,
        headers: dict | None,
        max_retries: int = 6,
        timeout: int = 10,
        **kwargs
    ):
        if max_retries < 0:
            raise RuntimeError
        try:
            return requests.get(url=url, headers=headers, **kwargs, timeout=timeout)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return cls.get(url=url, headers=headers, max_retries=max_retries - 1, timeout=timeout + 20, **kwargs)

    @classmethod
    def post(
            cls,
            url: str,
            json: dict,
            headers: dict,
            max_retries: int = 6,
            timeout: int = 10,
            **kwargs
    ):
        if max_retries < 0:
            raise RuntimeError
        try:
            response = requests.post(url=url, json=json, headers=headers, **kwargs, timeout=timeout)
            return response
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return cls.post(
                url=url,
                json=json,
                headers=headers,
                max_retries=max_retries - 1,
                timeout=timeout + 20,
                **kwargs
            )
