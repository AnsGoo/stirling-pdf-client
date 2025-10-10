from httpx import Client, Response
from .type import Status, LoadCount
from typing import Any, List, Optional
from .mix import MixApi
from .utils import requires_server_version




class InfoApi(MixApi):
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def get_uptime(self) -> str:
        url = "/api/v1/info/uptime"
        resp: Response = self.__client.request(method="GET", url=url)

        return resp.text


    def get_status(self) -> Status:
        url = "/api/v1/info/status"
        resp: Response = self.__client.request(method="GET", url=url)
        # 将JSON响应转换为Status类型
        status_data = resp.json()
        return Status(
            version=status_data.get("version", ""), status=status_data.get("status", "")
        )

    @requires_server_version("1.3.2")
    def get_load(self, endpoint: Optional[str] = None) -> int:
        url = "/api/v1/info/load"
        resp: Response = self.__client.request(
            method="GET", url=url, params={"endpoint": endpoint}
        )
        # 将JSON响应转换为Status类型
        status_data = resp.json()
        return status_data

    def get_load_unique(self, endpoint: Optional[str] = None) -> int:
        url = "/api/v1/info/load/unique"
        resp: Response = self.__client.request(
            method="GET", url=url, params={"endpoint": endpoint}
        )
        # 将JSON响应转换为Status类型
        status_data = resp.json()
        return status_data

    def get_load_all(self, endpoint: Optional[str] = None) -> List[LoadCount]:
        url = "/api/v1/info/load/all"
        resp: Response = self.__client.request(
            method="GET", url=url, params={"endpoint": endpoint}
        )
        # 将JSON响应转换为Status类型
        data: List[Any] = resp.json()
        return list(
            map(
                lambda el: LoadCount(
                    endpoint=el.get("endpoint", ""), count=el.get("count", 0)
                ),
                data,
            )
        )

    def get_load_all_unique(self) -> List[LoadCount]:
        url = "/api/v1/info/load/all/unique"
        resp: Response = self.__client.request(method="GET", url=url)
        # 将JSON响应转换为Status类型
        data: List[Any] = resp.json()
        return list(
            map(
                lambda el: LoadCount(
                    endpoint=el.get("endpoint", ""), count=el.get("count", 0)
                ),
                data,
            )
        )
