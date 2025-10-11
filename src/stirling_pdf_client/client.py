from typing import Optional
from httpx import Client

from stirling_pdf_client.utils import validate_response

from .convert import ConvertApi
from .info import InfoApi
from .security import SecurityApi
from .misc import MiscApi
from .general import GeneralApi
from .filter import FilterApi


class ProxyClient(Client):
    """
    代理客户端类，继承自httpx.Client，增强了版本检查、请求验证和状态更新功能。

    该类自动获取并维护服务器版本信息，验证所有响应，并在状态变更时更新。

    Attributes:
        version: 服务器版本号
        server_status: 服务器状态
    """

    version: Optional[str] = None
    server_status: Optional[str] = None

    def __init__(self, base_url: str, **kwargs):
        """
        初始化ProxyClient实例。

        Args:
            base_url: Stirling PDF服务器的基础URL
            **kwargs: 传递给httpx.Client的其他参数
        """
        super().__init__(base_url=base_url, **kwargs)
        status = self.__get_status()
        self.server_status = status.get("status", None)
        self.version = status.get("version", None)

    def request(self, *args, **kwargs):
        """
        发送HTTP请求，并进行响应验证和状态更新。

        Args:
            *args: 传递给httpx.Client.request的位置参数
            **kwargs: 传递给httpx.Client.request的关键字参数

        Returns:
            Response: HTTP响应对象

        Raises:
            ValueError: 如果版本信息为空
            Exception: 如果响应验证失败
        """
        if not self.version:
            raise ValueError("version is empty")
        response = super().request(*args, **kwargs)
        validate_response(response)
        if kwargs.get("url") == "/api/v1/info/status":
            resp = response.json()
            self.update_status(
                version=resp.get("version", None),
                server_status=resp.get("status", None),
            )
        return response

    def __get_status(self) -> dict:
        """
        获取服务器状态信息。

        Returns:
            dict: 包含服务器版本和状态的字典

        Raises:
            Exception: 如果请求失败或响应验证失败
        """
        url = "/api/v1/info/status"
        resp = super().request(method="GET", url=url)
        validate_response(resp)
        result = resp.json()
        return result

    def update_status(self, version: Optional[str], server_status: Optional[str]):
        """
        更新服务器状态信息。

        Args:
            version: 新的服务器版本号
            server_status: 新的服务器状态
        """
        self.server_status = server_status
        self.version = version


class StirlingPDFClient:
    """
    Stirling PDF客户端主类，提供对所有API功能模块的访问。

    该类是与Stirling PDF服务器交互的主要入口点，初始化各个API模块实例。

    Attributes:
        base_url: Stirling PDF服务器的基础URL
        info: 信息查询API实例
        convert: 文件转换API实例
        security: 安全相关API实例
        misc: 其他杂项API实例
        general: 通用PDF操作API实例
        filter: 过滤相关API实例
    """

    def __init__(
        self,
        base_url: str,
        **kwargs,
    ):
        """
        初始化StirlingPDFClient实例。

        Args:
            base_url: Stirling PDF服务器的基础URL
            **kwargs: 传递给ProxyClient的其他参数
        """
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
