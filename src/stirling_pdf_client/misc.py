from httpx import Client, Response
from typing import Literal, Optional, List
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


@dataclass
class OcrPdfOptions:
    sidecar: Optional[bool] = True
    deskew: Optional[bool] = True
    clean: Optional[bool] = True
    clean_final: Optional[bool] = True
    remove_images_after: Optional[bool] = True


@dataclass
class StampOptions:
    page_numbers: Optional[str] = "all"
    stamp_type: Optional[Literal["text", "image"]] = "text"
    stamp_text: Optional[str] = None
    stamp_image: Optional[Path] = None
    alphabet: Optional[Literal["roman", "arabic", "japanese", "chinese", "korean"]] = (
        "roman"
    )
    font_size: Optional[int] = 30
    rotation: Optional[int] = 0
    opacity: Optional[float] = 0.5
    override_x: Optional[float] = -1
    override_y: Optional[float] = -1
    position: Optional[
        Literal[
            "topLeft",
            "topRight",
            "topCenter",
            "bottomLeft",
            "bottomRight",
            "bottomCenter",
            "middleLeft",
            "middleRight",
            "middleCenter",
        ]
    ] = "middleCenter"
    custom_margin: Optional[Literal["medium", "small", "large", "x-large"]] = "medium"
    custom_color: Optional[str] = "#d3d3d3"


@dataclass
class ImageOptions:
    image_file: Path
    page_numbers: Optional[str] = "all"
    x: Optional[float] = 0
    y: Optional[float] = 0
    every_page: Optional[bool] = False


class MiscApi:
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def update_metadata(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        delete_all: Optional[bool] = False,
        options: Optional[UpdateMetadataOptions] = None,
    ) -> str:
        url = "/api/v1/misc/update-metadata"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")

        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
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
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> str:
        url = "/api/v1/misc/unlock-pdf-forms"
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
        file_id: Optional[str] = None,
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
            "fileId": file_id,
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

    def repair(
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> str:
        url = "/api/v1/misc/repair"
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
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def remove_blanks(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        threshold: Optional[int] = 10,
        white_percent: Optional[float] = 99.9,
    ) -> str:
        url = "/api/v1/misc/remove-blanks"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
            "threshold": threshold,
            "whitePercent": white_percent,
        }
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def orc_pdf(
        self,
        out_path: Path,
        languages: Optional[List[str]],
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        orc_type: Literal["skip-text", "force-ocr", "Normal"] = "skip-text",
        orc_render_type: Literal["hocr", "sandwich"] = "hocr",
        options: Optional[OcrPdfOptions] = {
            "sidecar": True,
            "deskew": True,
            "clean": True,
            "clean_final": True,
            "remove_images_after": True,
        },
    ) -> str:
        url = "/api/v1/misc/orc-pdf"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
            "languages": languages,
            "orcType": orc_type,
            "orcRenderType": orc_render_type,
        }
        if options:
            data.update(
                {
                    "sidecar": options.sidecar,
                    "deskew": options.deskew,
                    "clean": options.clean,
                    "clean_final": options.clean_final,
                    "remove_images_after": options.remove_images_after,
                }
            )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def flatten(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        flatten_only_forms: Optional[bool] = False,
    ) -> str:
        url = "/api/v1/misc/flatten"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id, "flattenOnlyForms": flatten_only_forms}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def extract_images(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        format: Literal["png", "jpg", "jpeg", "gif"] = "png",
        allow_duplicates: Optional[bool] = False,
    ) -> str:
        url = "/api/v1/misc/extract-images"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
            "format": format,
            "allowDuplicates": allow_duplicates,
        }
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def extract_image_scans(
        self,
        out_path: Path,
        file_input: Path,
        angle_threshold: Optional[int] = 5,
        tolerance: Optional[int] = 20,
        min_area: Optional[int] = 8000,
        min_contour_area: Optional[int] = 500,
        border_size: Optional[int] = 1,
    ) -> str:
        url = "/api/v1/misc/extract-image-scans"
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "angleThreshold": angle_threshold,
            "tolerance": tolerance,
            "minArea": min_area,
            "minContourArea": min_contour_area,
            "borderSize": border_size,
        }
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def decompress_pdf(
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> str:
        url = "/api/v1/misc/decompress-pdf"
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
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def compress_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        optimize_level: Optional[int] = 5,
        expected_output_size: Optional[int] = 25,
        linearize: Optional[bool] = False,
        normalize: Optional[bool] = False,
        grayscale: Optional[bool] = False,
    ) -> str:
        url = "/api/v1/misc/compress-pdf"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
            "optimizeLevel": optimize_level,
            "expectedOutputSize": f"{expected_output_size}kb",
            "linearize": linearize,
            "normalize": normalize,
            "grayscale": grayscale,
        }
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def auto_split_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
    ) -> str:
        url = "/api/v1/misc/auto-split-pdf"
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
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def auto_rename(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        use_first_text_as_fallback: Optional[bool] = False,
    ) -> str:
        url = "/api/v1/misc/auto-rename"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {"fileId": file_id, "useFirstTextAsFallback": use_first_text_as_fallback}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def add_stamp(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        options: Optional[StampOptions] = StampOptions(),
    ) -> str:
        url = "/api/v1/misc/add-stamp"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
        }
        POSITION_MAPPING = {
            "topLeft": 7,
            "topRight": 9,
            "topCenter": 8,
            "bottomLeft": 1,
            "bottomRight": 3,
            "bottomCenter": 2,
            "middleLeft": 4,
            "middleRight": 6,
            "middleCenter": 5,
        }
        data.update(
            {
                "pageNumbers": options.page_numbers,
                "stampType": options.stamp_type,
                "stampText": options.stamp_text,
                "stampImage": open(options.stamp_image, "rb"),
                "alphabet": options.alphabet,
                "position": POSITION_MAPPING[options.position],
                "customMargin": options.custom_margin,
                "customColor": options.custom_color,
                "rotation": options.rotation,
                "fontSize": options.font_size,
                "override_x": options.override_x,
                "override_y": options.override_y,
                "opacity": options.opacity,
            }
        )

        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def add_image(
        self,
        out_path: Path,
        file_input: Optional[Path],
        options: Optional[ImageOptions],
        file_id: Optional[str] = None,
    ) -> str:
        url = "/api/v1/misc/add-image"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        files = {"fileInput": file}
        data = {
            "fileId": file_id,
        }
        with open(options.image_file, "rb") as f:
            files["image"] = f
        data.update(
            {
                "pageNumbers": options.page_numbers,
                "x": options.x,
                "y": options.y,
                "everyPage": options.every_page,
            }
        )
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text

    def add_attachments(
        self,
        out_path: Path,
        file_input: Optional[Path],
        attachments: List[Path],
        file_id: Optional[str] = None,
    ) -> str:
        url = "/api/v1/misc/add-attachments"
        if file_input is None and file_id is None:
            raise ValueError("file_input and file_id must be provided one of")
        file = None
        if file_input:
            file = open(file_input, "rb")
        attachments_files = []
        for attachment in attachments:
            attachments_files.append(open(attachment, "rb"))
        files = {"fileInput": file, "attachments": attachments_files}
        data = {"fileId": file_id}
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        for attachment_file in attachments_files:
            attachment_file.close()
        save_file(resp=resp, out_path=out_path)
        if file:
            file.close()
        return resp.text
