from operator import truediv
from os import name
from httpx import Client, Response
from typing import List, Literal, Optional
from pathlib import Path
from dataclasses import dataclass
from utils import save_file


@dataclass
class ValidateSignatureResult:
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
    remove_java_scripts: bool = False
    remove_embedded_files: bool = False
    remove_metadata: bool = False
    remove_links: bool = False
    remove_xmp_metadata: bool = False
    remove_fonts: bool = False


@dataclass
class ConvertPdfToImageOption:
    x: float = 0.1
    y: float = 0.1
    width: int = 0.1
    height: int = 0.1
    page: int = 0
    color: str = "#000000"


@dataclass
class RedactOption:
    page_numbers: str = "all"
    redactions: bool = False
    convert_pdf_to_image: ConvertPdfToImageOption
    pageRedactionColor: str = "#000000"


@dataclass
class CertSignOption:
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


class SecurityApi:
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def validate_signature(
        self,
        file_input: Optional[Path],
        cert_file: [Path],
        fileId: Optional[str] = None,
    ) -> ValidateSignatureResult:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": fileId}
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
        fileId: Optional[str] = None,
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": fileId,
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
        fileId: Optional[str] = None,
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": fileId, "password": password}
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
        fileId: Optional[str] = None,
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": fileId,
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
        fileId: Optional[str] = None,
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": fileId,
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
        self, file_input: Optional[Path], fileId: Optional[str] = None
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": fileId,
        }
        url = "/api/v1/security/get-info-on-pdf"
        resp: Response = self.__client.request(
            method="POST", url=url, files={"fileInput": file}, data=data
        )
        if file:
            file.close()
        return resp.text

    def add_password(
        self,
        out_path: Path,
        password: str,
        owner_password: str,
        options: AddPasswordOption,
        file_input: Optional[Path],
        key_length: int = 256,
        fileId: Optional[str] = None,
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {
            "fileId": fileId,
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
        fileId: Optional[str] = None,
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": fileId}
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
        fileId: Optional[str] = None,
        options: CertSignOption = CertSignOption(),
    ) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        data = {"fileId": fileId}
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
