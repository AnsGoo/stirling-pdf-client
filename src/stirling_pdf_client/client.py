from httpx import Client

from .convert import ConvertApi
from .info import InfoApi


class StirlingPDFClient:
    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url
        self.__client = Client(
            base_url=base_url,
            headers={
                "contentType": "application/json",
                "referer": base_url,
                "accept": "*/*",
            },
            timeout=3600 * 30,
        )
        self.info = InfoApi(self.__client)
        self.convert = ConvertApi(self.__client)
