from typing import List, Literal, Optional
from pathlib import Path
from dataclasses import dataclass, field
from httpx import Client, Response
from .utils import save_file
from .mix import MixApi


@dataclass
class ValidateSignatureResult:
    """
    证书签名验证结果类，包含签名验证的详细信息。

    Attributes:
        valid: 签名是否有效
        signerName: 签名者名称
        signatureDate: 签名日期
        reason: 签名原因
        location: 签名位置
        errorMessage: 错误信息
        chainValid: 证书链是否有效
        trustValid: 信任链是否有效
        notExpired: 证书是否未过期
        notRevoked: 证书是否未被撤销
        issuerDN: 发行者名称
        subjectDN: 主题名称
        serialNumber: 序列号
        validFrom: 有效起始日期
        validUntil: 有效截止日期
        signatureAlgorithm: 签名算法
        keySize: 密钥大小
        version: 版本
        keyUsages: 密钥用途列表
        selfSigned: 是否自签名
    """

    valid: bool
    signerName: str
    signatureDate: str
    reason: str
    location: str
    errorMessage: str
    chainValid: bool
    trustValid: bool
    notExpired: bool
    notRevoked: bool
    issuerDN: str
    subjectDN: str
    serialNumber: str
    validFrom: str
    validUntil: str
    signatureAlgorithm: str
    keySize: int
    version: str
    keyUsages: List[str]
    selfSigned: bool


@dataclass
class SanitizePdfOption:
    """
    PDF清理选项类，定义了如何清理PDF文件中的敏感内容。

    Attributes:
        remove_java_scripts: 是否移除JavaScript
        remove_embedded_files: 是否移除嵌入文件
        remove_metadata: 是否移除元数据
        remove_links: 是否移除链接
        remove_xmp_metadata: 是否移除XMP元数据
        remove_fonts: 是否移除字体
    """

    remove_java_scripts: bool = False
    remove_embedded_files: bool = False
    remove_metadata: bool = False
    remove_links: bool = False
    remove_xmp_metadata: bool = False
    remove_fonts: bool = False


@dataclass
class ConvertPdfToImageOption:
    """
    PDF转换为图像的选项类，定义了转换参数。

    Attributes:
        x: X坐标位置
        y: Y坐标位置
        width: 宽度
        height: 高度
        page: 页码
        color: 颜色
    """

    x: float = 0.1
    y: float = 0.1
    width: int = 0.1
    height: int = 0.1
    page: int = 0
    color: str = "#000000"


@dataclass
class RedactOption:
    """
    PDF内容编辑选项类，定义了如何编辑PDF内容。

    Attributes:
        page_numbers: 页码范围，默认为"all"（所有页面）
        redactions: 是否进行编辑
        convert_pdf_to_image: 转换为图像的选项
        pageRedactionColor: 页面编辑颜色
    """

    page_numbers: str = "all"
    redactions: bool = False
    convert_pdf_to_image: ConvertPdfToImageOption = field(
        default_factory=ConvertPdfToImageOption
    )
    pageRedactionColor: str = "#000000"


@dataclass
class CertSignOption:
    """
    证书签名选项类，定义了如何为PDF添加证书签名。

    Attributes:
        cert_type: 证书类型
        private_key_file: 私钥文件路径
        cert_file: 证书文件路径
        p12_file: P12文件路径
        jks_file: JKS文件路径
        password: 密码
        show_signature: 是否显示签名
        reason: 签名原因
        location: 签名位置
        name: 签名者名称
        page_number: 签名页码
        show_logo: 是否显示标志
    """

    cert_type: Literal["PEM", "PKCS12", "PFX", "JKS"] = "PEM"
    private_key_file: Optional[Path] = None
    cert_file: Optional[Path] = None
    p12_file: Optional[Path] = None
    jks_file: Optional[Path] = None
    password: Optional[str] = None
    show_signature: Optional[bool] = False
    reason: Optional[str] = None
    location: Optional[str] = None
    name: Optional[str] = None
    page_number: Optional[int] = 1
    show_logo: Optional[bool] = True


@dataclass
class AddPasswordOption:
    """
    添加密码选项类，定义了PDF文件的权限控制设置。

    Attributes:
        prevent_assembly: 是否阻止组装
        prevent_extract_content: 是否阻止提取内容
        prevent_extract_for_accessibility: 是否阻止为可访问性提取
        prevent_fill_in_form: 是否阻止填写表单
        prevent_modify: 是否阻止修改
        prevent_modify_annotations: 是否阻止修改注释
        prevent_printing: 是否阻止打印
        prevent_printing_faithful: 是否阻止高质量打印
    """

    prevent_assembly: Optional[bool] = False
    prevent_extract_content: Optional[bool] = False
    prevent_extract_for_accessibility: Optional[bool] = False
    prevent_fill_in_form: Optional[bool] = False
    prevent_modify: Optional[bool] = False
    prevent_modify_annotations: Optional[bool] = False
    prevent_printing: Optional[bool] = False
    prevent_printing_faithful: Optional[bool] = False


@dataclass
class AddWatermarkOption:
    """
    添加水印选项类，定义了如何为PDF添加水印。

    Attributes:
        watermark_type: 水印类型（文本或图像）
        watermark_text: 水印文本
        watermark_image: 水印图像路径
        alphabet: 字母类型
        font_size: 字体大小
        rotate: 旋转角度
        opacity: 透明度
        width_spacer: 宽度间隔
        height_spacer: 高度间隔
        custom_color: 自定义颜色
        convert_pdf_to_image: 是否转换为图像
    """

    watermark_type: Literal["text", "image"] = "text"
    watermark_text: Optional[str] = None
    watermark_image: Optional[Path] = None
    alphabet: Optional[Literal["chinese", "roman", "japanese", "korean", "arabic"]] = (
        "roman"
    )
    font_size: Optional[int] = 30
    rotate: Optional[int] = 0
    opacity: Optional[float] = 0.5
    width_spacer: Optional[int] = 50
    height_spacer: Optional[int] = 50
    custom_color: Optional[str] = "#d3d3d3"
    convert_pdf_to_image: Optional[bool] = False


class SecurityApi(MixApi):
    """
    安全相关API类，提供PDF文件的安全操作功能。

    该类继承自MixApi，提供签名验证、PDF清理、密码添加/移除等安全相关功能。

    Attributes:
        __client: 用于发送HTTP请求的客户端对象
    """

    __client: Client

    def __init__(self, client: Client) -> None:
        """
        初始化SecurityApi对象。

        Args:
            client: 用于发送HTTP请求的客户端对象
        """
        self.__client = client

    def validate_signature(
        self,
        cert_file: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
    ) -> ValidateSignatureResult:
        """
        验证PDF文件的数字签名。

        Args:
            cert_file: 证书文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            ValidateSignatureResult: 签名验证结果对象

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": file_id}
        cert = open(cert_file, "rb")
        files = {"fileInput": file, "certFile": cert}
        url = "/api/v1/security/validate-signature"
        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        cert.close()
        if file:
            file.close()
        return resp.json()

    def sanitize_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path],
        options: SanitizePdfOption,
        file_id: Optional[str] = None,
    ) -> str:
        """
        清理PDF文件中的敏感内容。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            options: 清理选项
            file_id: 替代文件输入的文件ID

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": file_id,
        }
        data.update(
            {
                "removeJavaScript": options.remove_java_scripts,
                "removeEmbeddedFiles": options.remove_embedded_files,
                "removeMetadata": options.remove_metadata,
                "removeLinks": options.remove_links,
                "removeXmpMetadata": options.remove_xmp_metadata,
                "removeFonts": options.remove_fonts,
            }
        )
        url = "/api/v1/security/sanitize-pdf"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        save_file(resp, out_path)
        return resp.text

    def remove_password(
        self,
        out_path: Path,
        password: str,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
    ) -> str:
        """
        移除PDF文件的密码保护。

        Args:
            out_path: 输出文件路径
            password: PDF文件的密码
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误或密码错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": file_id, "password": password}
        url = "/api/v1/security/remove-password"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        save_file(resp, out_path)
        return resp.text

    def remove_cert_sign(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
    ) -> str:
        """
        移除PDF文件的证书签名。

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
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": file_id,
        }
        url = "/api/v1/security/remove-cert-sign"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        save_file(resp, out_path)
        return resp.text

    def redact(
        self,
        out_path: Path,
        options: RedactOption,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
    ) -> str:
        """
        编辑PDF文件中的内容。

        Args:
            out_path: 输出文件路径
            options: 编辑选项
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
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": file_id,
        }
        data.update(
            {
                "pageNumbers": options.page_numbers,
                "redactions": options.redactions,
                "convertPdfToImage": {
                    "x": options.convert_pdf_to_image.x,
                    "y": options.convert_pdf_to_image.y,
                    "width": options.convert_pdf_to_image.width,
                    "height": options.convert_pdf_to_image.height,
                    "page": options.convert_pdf_to_image.page,
                    "color": options.convert_pdf_to_image.color,
                },
                "pageRedactionColor": options.pageRedactionColor,
            }
        )
        url = "/api/v1/security/redact"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        save_file(resp, out_path)
        return resp.text

    def get_info_on_pdf(
        self, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> str:
        """
        获取PDF文件的安全信息。

        Args:
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID

        Returns:
            str: PDF文件的安全信息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": file_id,
        }
        url = "/api/v1/security/get-info-on-pdf"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        return resp.json()

    def add_password(
        self,
        out_path: Path,
        password: str,
        owner_password: str,
        options: AddPasswordOption,
        file_input: Optional[Path],
        key_length: int = 256,
        file_id: Optional[str] = None,
    ) -> str:
        """
        为PDF文件添加密码保护。

        Args:
            out_path: 输出文件路径
            password: 用户密码
            owner_password: 所有者密码
            options: 权限控制选项
            file_input: PDF文件路径
            key_length: 密钥长度（默认256位）
            file_id: 替代文件输入的文件ID

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": file_id,
            "password": password,
            "ownerPassword": owner_password,
            "keyLength": key_length,
        }
        data.update(
            {
                "preventAssembly": options.prevent_assembly,
                "preventExtractContent": options.prevent_extract_content,
                "preventExtractForAccessibility": options.prevent_extract_for_accessibility,
                "preventFillInForm": options.prevent_fill_in_form,
                "preventModify": options.prevent_modify,
                "preventModifyAnnotations": options.prevent_modify_annotations,
                "preventPrinting": options.prevent_printing,
                "preventPrintingFaithful": options.prevent_printing_faithful,
            }
        )
        url = "/api/v1/security/add-password"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        save_file(resp, out_path)
        return resp.text

    def add_watermark(
        self,
        out_path: Path,
        options: AddWatermarkOption,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
    ) -> str:
        """
        为PDF文件添加水印。

        Args:
            out_path: 输出文件路径
            options: 水印选项
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
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": file_id}
        data.update(
            {
                "watermarkType": options.watermark_type,
                "watermarkText": options.watermark_text,
                "watermarkImage": options.watermark_image,
                "alphabet": options.alphabet,
                "fontSize": options.font_size,
                "rotate": options.rotate,
                "opacity": options.opacity,
                "widthSpacer": options.width_spacer,
                "heightSpacer": options.height_spacer,
                "customColor": options.custom_color,
                "convertPdfToImage": options.convert_pdf_to_image,
            }
        )
        url = "/api/v1/security/add-watermark"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        save_file(resp, out_path)
        return resp.text

    def cert_sign(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        options: CertSignOption = CertSignOption(),
    ) -> str:
        """
        为PDF文件添加证书签名。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            options: 证书签名选项

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": file_id}
        url = "/api/v1/security/cert-sign"
        data.update(
            {
                "certType": options.cert_type,
                "privateKeyFile": options.private_key_file,
                "certFile": options.cert_file,
                "p12File": options.p12_file,
                "jksFile": options.jks_file,
                "password": options.password,
                "showSignature": options.show_signature,
                "reason": options.reason,
                "location": options.location,
                "name": options.name,
                "pageNumber": options.page_number,
                "showLogo": options.show_logo,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        save_file(resp, out_path)
        return resp.text
