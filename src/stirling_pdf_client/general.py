from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Literal, List
from httpx import Client, Response
from .utils import save_file
from .mix import MixApi


@dataclass
class SplitPdfBySectionsOptions:
    """
    按部分分割PDF的选项类。

    Attributes:
        horizontal_divisions: 水平分割数
        vertical_divisions: 垂直分割数
        merge: 是否合并结果
    """

    horizontal_divisions: Optional[int] = 0
    vertical_divisions: Optional[int] = 1
    merge: Optional[bool] = True


@dataclass
class SplitPdfByChaptersOptions:
    """
    按章节分割PDF的选项类。

    Attributes:
        include_metadata: 是否包含元数据
        allow_duplicates: 是否允许重复
        bookmark_level: 书签级别
    """

    include_metadata: Optional[bool] = True
    allow_duplicates: Optional[bool] = True
    bookmark_level: Optional[int] = 2


@dataclass
class OverlayPdfOptions:
    """
    叠加PDF的选项类。

    Attributes:
        overlay_mode: 叠加模式
        counts: 计数列表
        overlay_position: 叠加位置
        overlay_files: 要叠加的文件列表
    """

    overlay_mode: Optional[
        Literal["SequentialOverlay", "InterleavedOverlay", "FixedRepeatOverlay"]
    ] = "SequentialOverlay"
    counts: Optional[List[int]] = field(default_factory=list)
    overlay_position: int = 0
    overlay_files: List[Path] = field(default_factory=list)


@dataclass
class CropBox:
    """
    裁剪框选项类。

    Attributes:
        x: X坐标
        y: Y坐标
        width: 宽度
        height: 高度
    """

    x: Optional[int] = 0
    y: Optional[int] = 0
    width: Optional[int] = 0
    height: Optional[int] = 0


class GeneralApi(MixApi):
    """
    通用API类，提供PDF文件的基础操作功能。

    该类继承自MixApi，提供PDF的分割、合并、旋转、裁剪等多种基础操作。

    Attributes:
        __client: 用于发送HTTP请求的客户端对象
    """

    __client: Client

    def __init__(self, client: Client) -> None:
        """
        初始化GeneralApi对象。

        Args:
            client: 用于发送HTTP请求的客户端对象
        """
        self.__client = client

    def split_pdf_by_sections(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        options: SplitPdfBySectionsOptions = SplitPdfBySectionsOptions(),
    ) -> str:
        """
        按部分分割PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            options: 分割选项

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/split-pdf-by-sections"
        data = {}
        files = {}
        file = None
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        data.update(
            {
                "horizontalDivisions": options.horizontal_divisions,
                "verticalDivisions": options.vertical_divisions,
                "merge": options.merge,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def split_pdf_by_chapters(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        options: SplitPdfByChaptersOptions = SplitPdfByChaptersOptions(),
    ) -> str:
        """
        按章节分割PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            options: 分割选项

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/split-pdf-by-chapters"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        data.update(
            {
                "includeMetadata": options.include_metadata,
                "allowDuplicates": options.allow_duplicates,
                "bookmarkLevel": options.bookmark_level,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def split_pages(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_numbers: str = "all",
    ) -> str:
        """
        分割PDF文件的页面。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_numbers: 要分割的页码范围

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/split-pages"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        data.update(
            {
                "pageNumbers": page_numbers,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def split_by_size_or_count(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        split_type: Literal["size", "page", "document"] = "size",
        split_value: str = "10MB",
    ) -> str:
        """
        按大小或页数分割PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            split_type: 分割类型（大小、页数、文档）
            split_value: 分割值

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/split-by-size-or-count"
        SPLIT_TYPE_MAP = {
            "size": 0,
            "page": 1,
            "document": 2,
        }
        data = {
            "splitType": SPLIT_TYPE_MAP[split_type],
            "splitValue": split_value,
        }
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def scale_page(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_size: Literal[
            "A0", "A1", "A2", "A3", "A4", "A5", "A6", "LETTER", "LEGAL", "KEEP"
        ] = "A4",
        scale_factor: float = 1.0,
    ) -> str:
        """
        缩放PDF页面大小。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_size: 页面大小
            scale_factor: 缩放因子

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/scale-page"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        data.update(
            {
                "pageSize": page_size,
                "scale": scale_factor,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def rotate_page(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        angle: Literal[0, 90, 180, 270] = 90,
    ) -> str:
        """
        旋转PDF页面。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            angle: 旋转角度

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/rotate-page"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        data.update(
            {
                "angle": angle,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def remove_pages(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_numbers: str = "all",
    ) -> str:
        """
        从PDF文件中删除页面。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_numbers: 要删除的页码范围

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/remove-pages"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        data.update(
            {
                "pageNumbers": page_numbers,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def remove_image_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
    ) -> str:
        """
        从PDF文件中删除所有图像。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/remove-image-pdf"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def rearrange_page(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_numbers: str = "all",
        custom_mode: Literal[
            "CUSTOM",
            "SIDE_STITCH_BOOKLET_SORT",
            "REVERSE_ORDER",
            "DUPLEX_SORT",
            "BOOKLET_SORT",
            "ODD_EVEN_SPLIT",
            "ODD_EVEN_MERGE",
            "REMOVE_FIRST",
            "REMOVE_LAST",
            "REMOVE_FIRST_AND_LAST",
            "DUPLICATE",
        ] = "CUSTOM",
    ) -> str:
        """
        重新排列PDF页面顺序。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_numbers: 页码范围
            custom_mode: 自定义模式

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/rearrange-page"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        data.update(
            {
                "pageNumbers": page_numbers,
                "customMode": custom_mode,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def pdf_to_single_page(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
    ) -> str:
        """
        将PDF转换为单页文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/pdf-to-single-page"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def overlay_pdfs(
        self,
        out_path: Path,
        options: OverlayPdfOptions,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
    ) -> str:
        """
        在PDF文件上叠加其他PDF文件。

        Args:
            out_path: 输出文件路径
            options: 叠加选项
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/overlay-pdfs"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if file_id is not None:
            data["fileId"] = file_id

        overlay_files = []
        if options.overlay_files:
            overlay_files = [open(f, "rb") for f in options.overlay_files]

        files.update({"overlayFiles": overlay_files})
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        if overlay_files:
            for f in overlay_files:
                f.close()
        return resp.text

    def merge_pdfs(
        self,
        out_path: List[Path],
        file_inputs: List[Path],
        sort_type: Literal[
            "orderProvided",
            "byFileName",
            "byDateModified",
            "byDateCreated",
            "byPDFTitle",
        ] = "orderProvided",
        remove_cert_sign: bool = True,
        generate_toc: Optional[bool] = None,
    ) -> str:
        """
        合并多个PDF文件。

        Args:
            out_path: 输出文件路径
            file_inputs: 要合并的PDF文件列表
            sort_type: 排序类型
            remove_cert_sign: 是否移除证书签名
            generate_toc: 是否生成目录

        Returns:
            str: 操作结果消息

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/general/merge-pdfs"
        data = {}
        files = {}
        files["fileInputs"] = [open(f, "rb") for f in file_inputs]
        data.update(
            {
                "sortType": sort_type,
                "removeCertSign": remove_cert_sign,
                "generateToc": generate_toc,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        for f in file_inputs:
            f.close()
        return resp.text

    def extract_bookmarks(self, out_path: Path, file: Path) -> str:
        """
        从PDF文件中提取书签。

        Args:
            out_path: 输出文件路径
            file: PDF文件路径

        Returns:
            str: 操作结果消息

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/general/extract-bookmarks"
        file = None
        files = {}
        file_handle = open(file, "rb")
        files["fileInput"] = file_handle
        resp: Response = self.__client.request(method="POST", url=url, files=files)
        if file_handle is not None:
            file_handle.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def crop(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        options: CropBox = CropBox(),
    ) -> str:
        """
        裁剪PDF页面。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            options: 裁剪框选项

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/general/crop"
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file

        data = {}
        if file_id is not None:
            data["fileId"] = file_id

        data.update(
            {
                "x": options.x,
                "y": options.y,
                "width": options.width,
                "height": options.height,
            }
        )

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=options.model_dump()
        )
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text
