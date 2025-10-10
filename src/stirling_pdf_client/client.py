from httpx import Client

from .convert import ConvertApi
from .info import InfoApi
from .security import SecurityApi
from .misc import MiscApi
from .general import GeneralApi
from .filter import FilterApi


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
        self.security = SecurityApi(self.__client)
        self.misc = MiscApi(self.__client)
        self.general = GeneralApi(self.__client)
        self.filter = FilterApi(self.__client)
