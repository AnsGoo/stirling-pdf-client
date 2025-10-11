from httpx import Client, Response
from .type import Status, LoadCount
from typing import Any, List, Optional
from .mix import MixApi
from .utils import requires_server_version


class InfoApi(MixApi):
    """
    信息查询API类，提供获取Stirling PDF服务器各种信息的功能。

    该类继承自MixApi，用于获取服务器运行时间、状态、负载等信息。

    Attributes:
        __client: 用于发送HTTP请求的客户端对象
    """

    __client: Client

    def __init__(self, client: Client) -> None:
        """
        初始化InfoApi对象。

        Args:
            client: 用于发送HTTP请求的客户端对象
        """
        self.__client = client

    def get_uptime(self) -> str:
        """
        获取服务器的运行时间。

        Returns:
            str: 服务器运行时间的字符串表示

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/info/uptime"
        resp: Response = self.__client.request(method="GET", url=url)
        return resp.text

    def get_status(self) -> Status:
        """
        获取服务器的状态信息。

        Returns:
            Status: 包含服务器版本和状态的对象

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/info/status"
        resp: Response = self.__client.request(method="GET", url=url)
        # 将JSON响应转换为Status类型
        status_data = resp.json()
        return Status(
            version=status_data.get("version", ""), status=status_data.get("status", "")
        )

    @requires_server_version("1.3.2")
    def get_load(self, endpoint: Optional[str] = None) -> int:
        """
        获取服务器的负载信息。

        该方法需要服务器版本至少为1.3.2。

        Args:
            endpoint: 可选的端点名称，用于过滤特定端点的负载信息

        Returns:
            int: 服务器负载计数

        Raises:
            Exception: 如果服务器响应错误或版本不满足要求
        """
        url = "/api/v1/info/load"
        resp: Response = self.__client.request(
            method="GET", url=url, params={"endpoint": endpoint}
        )
        # 将JSON响应转换为Status类型
        status_data = resp.json()
        return status_data

    def get_load_unique(self, endpoint: Optional[str] = None) -> int:
        """
        获取服务器的唯一负载信息（按IP地址统计）。

        Args:
            endpoint: 可选的端点名称，用于过滤特定端点的负载信息

        Returns:
            int: 唯一负载计数（基于IP地址）

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/info/load/unique"
        resp: Response = self.__client.request(
            method="GET", url=url, params={"endpoint": endpoint}
        )
        # 将JSON响应转换为Status类型
        status_data = resp.json()
        return status_data

    def get_load_all(self, endpoint: Optional[str] = None) -> List[LoadCount]:
        """
        获取所有端点的负载信息。

        Args:
            endpoint: 可选的端点名称，用于过滤特定端点的负载信息

        Returns:
            List[LoadCount]: 包含每个端点负载计数的列表

        Raises:
            Exception: 如果服务器响应错误
        """
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
        """
        获取所有端点的唯一负载信息（按IP地址统计）。

        Returns:
            List[LoadCount]: 包含每个端点唯一负载计数的列表

        Raises:
            Exception: 如果服务器响应错误
        """
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
