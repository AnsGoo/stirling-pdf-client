from token import OP
from httpx import Client, Response
from typing import Literal, Optional
from pathlib import Path
from dataclasses import dataclass
from .utils import save_file


@dataclass
class UpdateMetadataOptions:
    author: Optional[str] = None
    creation_date: Optional[str] = None
    creator: Optional[str] = None
    keywords: Optional[str] = None
    modification_date: Optional[str] = None
    producer: Optional[str] = None
    subject: Optional[str] = None
    title: Optional[str] = None
    trapped: Optional[bool] = None
    all_request_params: Optional[dict] = None


@dataclass
class ScannerEffectOption:
    border: Optional[int] = 20
    rotate: Optional[int] = 0
    rotate_variance: Optional[int] = 0
    brightness: Optional[float] = 1
    contrast: Optional[float] = 1
    blur: Optional[float] = 1
    noise: Optional[float] = 8
    yellowish: Optional[bool] = False
    resolution: Optional[int] = 300
    advanced_enabled: Optional[bool] = False
    quality_value: Optional[int] = 0
    rotation_value: Optional[int] = 0


@dataclass
class ReplaceInvertPdfOptions:
    backGroundColor: Optional[str] = None
    textColor: Optional[str] = None


class MiscApi:
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def update_metadata(
        self,
        out_path: Path,
        file_input: Optional[Path],
        fileId: Optional[str] = None,
        delete_all: Optional[bool] = False,
        options: Optional[UpdateMetadataOptions] = None,
    ) -> str:
        url = "/api/v1/misc/update-metadata"
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")

        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": fileId,
            "deleteAll": delete_all,
        }
        if options:
            data.update(
                {
                    "author": options.author,
                    "creationDate": options.creation_date,
                    "creator": options.creator,
                    "keywords": options.keywords,
                    "modificationDate": options.modification_date,
                    "producer": options.producer,
                    "subject": options.subject,
                    "title": options.title,
                    "trapped": options.trapped,
                    "allRequestParams": options.all_request_params,
                }
            )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def unlock_pdf_forms(
        self, out_path: Path, file_input: Optional[Path], fileId: Optional[str] = None
    ) -> str:
        url = "/api/v1/misc/unlock-pdf-forms"
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")

        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": fileId}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def scanner_effect(
        self,
        out_path: Path,
        file_input: Path,
        quality: Literal["low", "medium", "high"] = "hight",
        rotation: Literal["none", "slight", "moderate", "severe"] = "none",
        options: Optional[ScannerEffectOption] = {
            "border": 20,
            "rotate": 0,
            "rotate_variance": 0,
            "brightness": 1,
            "contrast": 1,
            "blur": 1,
            "noise": 8,
            "yellowish": False,
            "resolution": 300,
            "advanced_enabled": False,
            "quality_value": 0,
            "rotation_value": 0,
        },
    ) -> str:
        url = "/api/v1/misc/scanner-effect"

        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"quality": quality, "rotation": rotation}
        if options:
            data.update(
                {
                    "border": options.border,
                    "rotate": options.rotate,
                    "rotate_variance": options.rotate_variance,
                    "brightness": options.brightness,
                    "contrast": options.contrast,
                    "blur": options.blur,
                    "noise": options.noise,
                    "yellowish": options.yellowish,
                    "resolution": options.resolution,
                    "advanced_enabled": options.advanced_enabled,
                    "quality_value": options.quality_value,
                    "rotation_value": options.rotation_value,
                }
            )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def replace_invert_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path],
        fileId: Optional[str] = None,
        replace_and_invert_option: Literal[
            "HIGH_CONTRAST_COLOR", "CUSTOM_COLOR", "FULL_INVERSION"
        ] = "HIGH_CONTRAST_COLOR",
        high_contrast_color_combination: Literal[
            "WHITE_TEXT_ON_BLACK", "BLACK_TEXT_ON_WHITE", "GREEN_TEXT_ON_BLACK"
        ] = "WHITE_TEXT_ON_BLACK",
        options: Optional[ReplaceInvertPdfOptions] = None,
    ) -> str:
        url = "/api/v1/misc/replace-invert-pdf"

        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": fileId,
            "replaceAndInvertOption": replace_and_invert_option,
            "highContrastColorCombination": high_contrast_color_combination,
        }
        if options:
            data.update(
                {
                    "backGroundColor": options.backGroundColor,
                    "textColor": options.textColor,
                }
            )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text
