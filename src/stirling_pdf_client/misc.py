from typing import Literal, Optional, List
from pathlib import Path
from dataclasses import dataclass
from httpx import Client, Response
from .utils import save_file
from .mix import MixApi


@dataclass
class UpdateMetadataOptions:
    """
    PDF元数据更新选项类，定义了PDF文件的元数据信息。

    Attributes:
        author: 作者
        creation_date: 创建日期
        creator: 创建者
        keywords: 关键词
        modification_date: 修改日期
        producer: 生产者
        subject: 主题
        title: 标题
        trapped: 是否包含陷印信息
        all_request_params: 所有请求参数
    """

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
    """
    扫描效果选项类，定义了如何为PDF添加扫描效果。

    Attributes:
        border: 边框大小
        rotate: 旋转角度
        rotate_variance: 旋转变化范围
        brightness: 亮度
        contrast: 对比度
        blur: 模糊度
        noise: 噪点
        yellowish: 是否泛黄
        resolution: 分辨率
        advanced_enabled: 是否启用高级选项
        quality_value: 质量值
        rotation_value: 旋转值
    """

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
    """
    PDF替换反转选项类，定义了PDF颜色替换和反转的设置。

    Attributes:
        backGroundColor: 背景颜色
        textColor: 文本颜色
    """

    backGroundColor: Optional[str] = None
    textColor: Optional[str] = None


@dataclass
class OcrPdfOptions:
    """
    OCR PDF选项类，定义了OCR识别的相关设置。

    Attributes:
        sidecar: 是否生成侧边文件
        deskew: 是否校正倾斜
        clean: 是否清理
        clean_final: 是否最终清理
        remove_images_after: 是否在OCR后移除图像
    """

    sidecar: Optional[bool] = True
    deskew: Optional[bool] = True
    clean: Optional[bool] = True
    clean_final: Optional[bool] = True
    remove_images_after: Optional[bool] = True


@dataclass
class StampOptions:
    """
    图章选项类，定义了如何为PDF添加图章。

    Attributes:
        page_numbers: 页码范围
        stamp_type: 图章类型（文本或图像）
        stamp_text: 图章文本
        stamp_image: 图章图像路径
        alphabet: 字母类型
        font_size: 字体大小
        rotation: 旋转角度
        opacity: 透明度
        override_x: 覆盖X坐标
        override_y: 覆盖Y坐标
        position: 图章位置
        custom_margin: 自定义边距
        custom_color: 自定义颜色
    """

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
    """
    图像添加选项类，定义了如何在PDF中添加图像。

    Attributes:
        image_file: 图像文件路径
        page_numbers: 页码范围
        x: X坐标
        y: Y坐标
        every_page: 是否在每一页添加
    """

    image_file: Path
    page_numbers: Optional[str] = "all"
    x: Optional[float] = 0
    y: Optional[float] = 0
    every_page: Optional[bool] = False


class MiscApi(MixApi):
    """
    杂项API类，提供PDF文件的各种操作功能。

    该类继承自MixApi，提供元数据更新、表单解锁、扫描效果、PDF修复、图像提取等多种功能。

    Attributes:
        __client: 用于发送HTTP请求的客户端对象
    """

    __client: Client

    def __init__(self, client: Client) -> None:
        """
        初始化MiscApi对象。

        Args:
            client: 用于发送HTTP请求的客户端对象
        """
        self.__client = client

    def update_metadata(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        delete_all: Optional[bool] = False,
        options: Optional[UpdateMetadataOptions] = None,
    ) -> Path:
        """
        更新PDF文件的元数据。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            delete_all: 是否删除所有现有元数据
            options: 元数据更新选项

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def unlock_pdf_forms(
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> Path:
        """
        解锁PDF表单，使表单可以编辑。

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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def scanner_effect(
        self,
        out_path: Path,
        file_input: Path,
        quality: Literal["low", "medium", "high"] = "high",
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
    ) -> Path:
        """
        为PDF文件添加扫描效果。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            quality: 质量设置（低、中、高）
            rotation: 旋转设置
            options: 扫描效果选项

        Returns:
            Path: 输出文件路径

        Raises:
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

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
    ) -> Path:
        """
        替换和反转PDF的颜色。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            replace_and_invert_option: 替换和反转选项
            high_contrast_color_combination: 高对比度颜色组合
            options: 自定义颜色选项

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def repair(
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> Path:
        """
        修复损坏的PDF文件。

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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def remove_blanks(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        threshold: Optional[int] = 10,
        white_percent: Optional[float] = 99.9,
    ) -> Path:
        """
        移除PDF文件中的空白页。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            threshold: 阈值设置
            white_percent: 空白百分比

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

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
    ) -> Path:
        """
        对PDF文件执行OCR（光学字符识别）。

        Args:
            out_path: 输出文件路径
            languages: 支持的语言列表
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            orc_type: OCR类型
            orc_render_type: OCR渲染类型
            options: OCR选项

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def flatten(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        flatten_only_forms: Optional[bool] = False,
    ) -> Path:
        """
        扁平化PDF文件中的表单和注释。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            flatten_only_forms: 是否只扁平化表单

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def extract_images(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        format: Literal["png", "jpg", "jpeg", "gif"] = "png",
        allow_duplicates: Optional[bool] = False,
    ) -> Path:
        """
        从PDF文件中提取图像。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            format: 输出图像格式
            allow_duplicates: 是否允许重复图像

        Returns:
            Path: 输出文件路径      

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def extract_image_scans(
        self,
        out_path: Path,
        file_input: Path,
        angle_threshold: Optional[int] = 5,
        tolerance: Optional[int] = 20,
        min_area: Optional[int] = 8000,
        min_contour_area: Optional[int] = 500,
        border_size: Optional[int] = 1,
    ) -> Path:  
        """
        从PDF文件中提取扫描图像。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            angle_threshold: 角度阈值
            tolerance: 容差
            min_area: 最小面积
            min_contour_area: 最小轮廓面积
            border_size: 边框大小

        Returns:
            Path: 输出文件路径  

        Raises:
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def decompress_pdf(
        self, out_path: Path, file_input: Optional[Path], file_id: Optional[str] = None
    ) -> Path:
        """
        解压缩PDF文件。

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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

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
    ) -> Path:
        """
        压缩PDF文件大小。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            optimize_level: 优化级别
            expected_output_size: 预期输出大小（KB）
            linearize: 是否线性化
            normalize: 是否标准化
            grayscale: 是否转换为灰度

        Returns:
            str: 操作结果消息

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def auto_split_pdf(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
    ) -> Path:
        """
        自动分割PDF文件。

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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def auto_rename(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        use_first_text_as_fallback: Optional[bool] = False,
    ) -> Path:
        """
        自动重命名PDF文件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            use_first_text_as_fallback: 是否使用首行文本作为备选

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def add_stamp(
        self,
        out_path: Path,
        file_input: Optional[Path],
        file_id: Optional[str] = None,
        options: Optional[StampOptions] = StampOptions(),
    ) -> Path:
        """
        为PDF文件添加图章。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            file_id: 替代文件输入的文件ID
            options: 图章选项

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def add_image(
        self,
        out_path: Path,
        file_input: Optional[Path],
        options: Optional[ImageOptions],
        file_id: Optional[str] = None,
    ) -> Path:
        """
        在PDF文件中添加图像。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            options: 图像添加选项
            file_id: 替代文件输入的文件ID

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)

    def add_attachments(
        self,
        out_path: Path,
        file_input: Optional[Path],
        attachments: List[Path],
        file_id: Optional[str] = None,
    ) -> Path:
        """
        向PDF文件添加附件。

        Args:
            out_path: 输出文件路径
            file_input: PDF文件路径
            attachments: 要添加的附件列表
            file_id: 替代文件输入的文件ID

        Returns:
            Path: 输出文件路径

        Raises:
            ValueError: 如果file_input和file_id都未提供
            Exception: 如果服务器响应错误
        """
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
        if file:
            file.close()
        return save_file(resp=resp, out_path=out_path)
