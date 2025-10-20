from httpx import Client, Response
from typing import Literal, Optional
from pathlib import Path
from .utils import save_file
from .mix import MixApi


class FilterApi(MixApi):
    """
    过滤相关API类，提供PDF文件的各种过滤功能。

    该类继承自MixApi，提供按页面大小、旋转角度、页数、文件大小、文本内容和图像内容等条件过滤PDF的功能。

    Attributes:
        __client: 用于发送HTTP请求的客户端对象
    """

    __client: Client

    def __init__(self, client: Client) -> None:
        """
        初始化FilterApi对象。

        Args:
            client: 用于发送HTTP请求的客户端对象
        """
        self.__client = client

    def filter_page_size(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        standard_page_size: Literal[
            "A0", "A1", "A2", "A3", "A4", "A5", "A6", "LETTER", "LEGAL"
        ] = "A4",
    ) -> Path:  
        """
        按页面大小过滤PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            comparator: 比较运算符（大于、等于、小于）
            standard_page_size: 标准页面大小

        Returns:
            Path: 输出文件路径  

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/filter/filter-page-size"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["standardPageSize"] = standard_page_size

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
            
        return save_file(resp=resp, out_path=out_path)

    def filter_page_rotation(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        rotation: int = 0,
    ) -> Path:  
        """
        按页面旋转角度过滤PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            comparator: 比较运算符（大于、等于、小于）
            rotation: 旋转角度

        Returns:
            Path: 输出文件路径  

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/filter/filter-page-rotation"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["rotation"] = rotation

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        return save_file(resp=resp, out_path=out_path)

    def filter_page_count(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        page_count: int = 0,
    ) -> Path:  
        """
        按页数过滤PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            comparator: 比较运算符（大于、等于、小于）
            page_count: 页数

        Returns:
            Path: 输出文件路径  

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/filter/filter-page-count"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["pageCount"] = page_count

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        return save_file(resp=resp, out_path=out_path)

    def filter_file_size(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        file_size: int = 0,
    ) -> Path:  
        """
        按文件大小过滤PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            comparator: 比较运算符（大于、等于、小于）
            file_size: 文件大小

        Returns:
            Path: 输出文件路径  

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/filter/filter-file-size"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["fileSize"] = file_size

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        return save_file(resp=resp, out_path=out_path)

    def filter_contains_text(
        self,
        out_path: Path,
        text: str,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_numbers: str = "all",
    ) -> Path:  
        """
        按包含的文本内容过滤PDF文件。

        Args:
            out_path: 输出文件路径
            text: 要查找的文本
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_numbers: 页码范围

        Returns:
            Path: 输出文件路径  

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/filter/filter-contains-text"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["text"] = text
        data["pageNumbers"] = page_numbers

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        return save_file(resp=resp, out_path=out_path)

    def filter_contains_image(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_numbers: str = "all",
    ) -> Path:  
        """
        按包含的图像内容过滤PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_numbers: 页码范围

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/filter/filter-contains-image"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["pageNumbers"] = page_numbers

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        return save_file(resp=resp, out_path=out_path)
