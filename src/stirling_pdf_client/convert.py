from pathlib import Path
from typing import Optional, Literal, List
from httpx import Client, Response
from .utils import save_file
from .mix import MixApi


class ConvertApi(MixApi):
    """
    转换相关API类，提供PDF文件和其他格式之间的转换功能。

    该类继承自MixApi，提供PDF与Word、PowerPoint、图片、HTML、Markdown等格式的相互转换功能。

    Attributes:
        __client: 用于发送HTTP请求的客户端对象
    """

    __client: Client

    def __init__(self, client: Client) -> None:
        """
        初始化ConvertApi对象。

        Args:
            client: 用于发送HTTP请求的客户端对象
        """
        self.__client = client

    def url_to_pdf(self, urlInput: str, out_path: Path) -> Path:
        """
        将URL转换为PDF文件。

        Args:
            urlInput: 要转换的URL
            out_path: 输出PDF文件路径

        Returns:
            str: 操作结果消息

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/url/pdf"
        resp: Response = self.__client.request(
            method="POST", url=url, data={"urlInput": urlInput}
        )
        return save_file(resp=resp, out_path=out_path)

    def pdf_to_xml(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
    ) -> Path:
        """
        将PDF文件转换为XML格式。

        Args:
            file_input: PDF文件路径
            file_id: 文件ID

        Returns:
            Path: 输出XML文件路径

        Raises:
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        url = "/api/v1/convert/pdf/xml"
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        with open(file_input, "rb") as file:
            files = {"fileInput": file}
            data = {"fileId": file_id}

            resp: Response = self.__client.request(
                method="POST", url=url, data=data, files=files
            )
            return save_file(resp=resp, out_path=out_path)

    def pdf_to_word(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        output_format: Optional[str] = "doc",
    ) -> Path:
        """
        将PDF文件转换为Word文档。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            output_format: 输出格式（'doc'或'docx'）

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供，或output_format不是'doc'或'docx'
            Exception: 如果服务器响应错误
        """
        # 确保output_format只能是'doc'或'docx'

        if output_format not in ["doc", "docx"]:
            raise ValueError("output_format must be either 'doc' or 'docx'")

        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")

        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        url = "/api/v1/convert/pdf/word"
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id, "outputFormat": output_format}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def advanced_pdf_conversion(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        advanced_options: Optional[dict] = None,
    ) -> Path:
        """
        高级PDF转换功能（仅在服务器版本 >= 2.0.0 时可用）。

        此方法展示了如何使用版本检查装饰器来限制功能可用性。
        在实际应用中，这可能是一个需要较新版本服务器支持的高级功能。

        Args:
            out_path: 输出文件路径
            file_input: 输入PDF文件路径
            file_id: 替代文件输入的文件ID
            advanced_options: 高级转换选项

        Returns:
            Path: 输出文件路径
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")

        url = "/api/v1/convert/pdf/advanced"
        file = None
        if file_input:
            file = open(file_input, "rb")

        files = {"fileInput": file}
        data = {"fileId": file_id}

        # 添加高级选项
        if advanced_options:
            data.update(advanced_options)

        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )

        if file:
            file.close()

        return save_file(resp=resp, out_path=out_path)

    def pdf_to_text(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        output_format: Optional[str] = "rtf",
    ) -> Path:
        """
        将PDF文件转换为文本文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            output_format: 输出格式

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/text"
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id, "outputFormat": output_format}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def pdf_to_presentation(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        output_format: Optional[str] = "ppt",
    ) -> Path:
        """
        将PDF文件转换为演示文稿。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            output_format: 输出格式（'ppt'或'pptx'）

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供，或output_format不是'ppt'或'pptx'
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/presentation"
        if output_format not in ["ppt", "pptx"]:
            raise ValueError("output_format must be either 'ppt' or 'pptx'")
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id, "outputFormat": output_format}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def pdf_to_pdfa(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        output_format: Optional[str] = "pdfa",
    ) -> Path:
        """
        将PDF文件转换为PDF/A格式（长期保存格式）。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            output_format: 输出格式（'pdfa'或'pdfa-1'）

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供，或output_format不是'pdfa'或'pdfa-1'
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/pdfa"
        if output_format not in ["pdfa", "pdfa-1"]:
            raise ValueError("output_format must be either 'pdfa' or 'pdfa-1'")
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id, "outputFormat": output_format}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def pdf_to_markdown(
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> Path:
        """
        将PDF文件转换为Markdown格式。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/markdown"
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def pdf_to_img(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        page_numbers: str = "all",
        image_format: Literal["png", "jpg", "jpeg", "gif", "webp"] = "png",
        single_or_multiple: Literal["single", "multiple"] = "multiple",
        color_type: Literal["color", "greyscale", "blackwhite"] = "color",
        dpi: int = 300,
        include_annotations: Optional[bool] = False,
    ) -> Path:
        """
        将PDF文件转换为图像文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_numbers: 要转换的页码范围
            image_format: 输出图像格式
            single_or_multiple: 单个或多个图像文件
            color_type: 颜色类型
            dpi: 图像分辨率
            include_annotations: 是否包含注释

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/img"
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
            "pageNumbers": page_numbers,
            "imageFormat": image_format,
            "singleOrMultiple": single_or_multiple,
            "colorType": color_type,
            "dpi": dpi,
            "includeAnnotations": include_annotations,
        }
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def pdf_to_html(
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> Path:
        """
        将PDF文件转换为HTML格式。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/html"
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def pdf_to_csv(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        page_numbers: str = "all",
    ) -> Path:
        """
        将PDF文件转换为CSV格式。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            page_numbers: 要转换的页码范围

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/csv"
        # 使用二进制模式打开文件，并使用上下文管理器自动关闭
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id, "pageNumber": page_numbers}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def markdown_to_pdf(self, out_path: Path, file_input: Path) -> Path:
        """
        将Markdown文件转换为PDF格式。

        Args:
            out_path: 输出文件路径
            file_input: Markdown文件路径

        Returns:
            Path: 输出文件路径

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/markdown/pdf"

        file = open(file_input, "rb")
        files = {"fileInput": file}
        resp: Response = self.__client.request(method="POST", url=url, files=files)
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def img_to_pdf(
        self,
        out_path: Path,
        file_input: List[Path],
        fit_option: Literal[
            "fillPage", "fitDocumentToImage", "maintainAspectRatio"
        ] = "fillPage",
        color_type: Literal["color", "greyscale", "blackwhite"] = "color",
        auto_rotate: Optional[bool] = False,
    ) -> Path:
        """
        将图像文件转换为PDF格式。

        Args:
            out_path: 输出文件路径
            file_input: 图像文件路径列表
            fit_option: 适配选项
            color_type: 颜色类型
            auto_rotate: 是否自动旋转

        Returns:
            Path: 输出文件路径

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/img/pdf"

        # 为每个文件创建一个文件对象
        files = []
        opened_files = []
        for file_path in file_input:
            file_obj = open(file_path, "rb")
            files.append(("fileInput", file_obj))
            opened_files.append(file_obj)

        data = {
            "fitOption": fit_option,
            "colorType": color_type,
            "autoRotate": auto_rotate,
        }
        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        # 确保所有文件都被关闭
        for file in opened_files:
            if not file.closed:
                file.close()

        return save_file(resp=resp, out_path=out_path)

    def html_to_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        zoom: Optional[float] = 1.0,
    ) -> Path:
        """
        将HTML文件转换为PDF格式。

        Args:
            out_path: 输出文件路径
            file_input: HTML文件路径
            file_id: 替代文件输入的文件ID
            zoom: 缩放比例

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/html/pdf"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")

        file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"zoom": zoom, "fileId": file_id}
        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file:
            file.close()

        return save_file(resp=resp, out_path=out_path)

    def file_to_pdf(self, out_path: Path, file_input: Path) -> Path:
        """
        将各种文件格式转换为PDF。

        Args:
            out_path: 输出文件路径
            file_input: 输入文件路径

        Returns:
            Path: 输出文件路径

        Raises:
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/file/pdf"
        file = open(file_input, "rb")
        files = {"fileInput": file}

        resp: Response = self.__client.request(method="POST", url=url, files=files)
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def eml_to_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        include_attachments: Optional[bool] = False,
        max_attachment_size_mb: Optional[int] = 10,
        download_html: Optional[bool] = False,
        include_all_recipients: Optional[bool] = True,
    ) -> Path:
        """
        将EML邮件文件转换为PDF格式。

        Args:
            out_path: 输出文件路径
            file_input: EML文件路径
            file_id: 替代文件输入的文件ID
            include_attachments: 是否包含附件
            max_attachment_size_mb: 最大附件大小（MB）
            download_html: 是否下载HTML内容
            include_all_recipients: 是否包含所有收件人

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        url = "/api/v1/convert/pdf/html"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "includeAttachments": include_attachments,
            "maxAttachmentSizeMB": max_attachment_size_mb,
            "downloadHtml": download_html,
            "includeAllRecipients": include_all_recipients,
        }

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)
