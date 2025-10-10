from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Literal, List
from httpx import Client, Response
from .utils import save_file


@dataclass
class SplitPdfBySectionsOptions:
    horizontal_divisions: Optional[int] = 0
    vertical_divisions: Optional[int] = 1
    merge: Optional[bool] = True


@dataclass
class SplitPdfByChaptersOptions:
    include_metadata: Optional[bool] = True
    allow_duplicates: Optional[bool] = True
    bookmark_level: Optional[int] = 2


@dataclass
class OverlayPdfOptions:
    overlay_mode: Optional[
        Literal["SequentialOverlay", "InterleavedOverlay", "FixedRepeatOverlay"]
    ] = "SequentialOverlay"
    counts: Optional[List[int]] = []
    overlay_position: int = 0
    overlay_files: List[Path] = []


@dataclass
class CropBox:
    x: Optional[int] = 0
    y: Optional[int] = 0
    width: Optional[int] = 0
    height: Optional[int] = 0


class GeneralApi:
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def split_pdf_by_sections(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        options: SplitPdfBySectionsOptions = SplitPdfBySectionsOptions(),
    ) -> str:
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
