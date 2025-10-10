from httpx import Client
from typing import Optional

from stirling_pdf_client.utils import validate_response

from .convert import ConvertApi
from .info import InfoApi
from .security import SecurityApi
from .misc import MiscApi
from .general import GeneralApi
from .filter import FilterApi


class ProxyClient(Client):
    version: Optional[str] = None
    server_status: Optional[str] = None
    def __init__(self, base_url: str, **kwargs):
        super().__init__(base_url=base_url, **kwargs)
        status =  self.__get_status()
        self.server_status = status.get("status", None)
        self.version = status.get("version", None)


    def request(self, *args, **kwargs):
        if not self.version:
            raise ValueError("version is empty")
        response = super().request(*args, **kwargs)
        validate_response(response)
        if kwargs.get("url") == "/api/v1/info/status":
            resp = response.json()
            self.update_status(version=resp.get("version", None), server_status=resp.get("status", None))
        return response

    
    def __get_status(self: str) -> str:
        url = "/api/v1/info/status"
        resp = super().request(method="GET", url=url)
        validate_response(resp)
        result =  resp.json()
        return result
    def update_status(self, version: str, server_status: str):
        self.server_status = server_status
        self.version = version


class StirlingPDFClient:
    def __init__(
        self,
        base_url: str,
        **kwargs,
    ):
        self.base_url = base_url
        self.__client = ProxyClient(
            base_url=base_url,
            headers={
                "contentType": "application/json",
                "referer": base_url,
                "accept": "*/*",
            },
            timeout=3600 * 30,
            **kwargs,
        )
        self.info = InfoApi(self.__client)
        self.convert = ConvertApi(self.__client)
        self.security = SecurityApi(self.__client)
        self.misc = MiscApi(self.__client)
        self.general = GeneralApi(self.__client)
        self.filter = FilterApi(self.__client)
