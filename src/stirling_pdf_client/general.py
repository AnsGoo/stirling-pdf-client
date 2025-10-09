
from dataclasses import dataclass
from heapq import merge
from operator import truediv
from pathlib import Path
from typing import Optional, Any, Literal, List
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


class GeneralApi:
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def split_pdf_by_sections(self, out_path: Path, file_input: Optional[Path] = None, fileId: Optional[str] = None, options: SplitPdfBySectionsOptions = SplitPdfBySectionsOptions()) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        url = "/api/v1/general/split-pdf-by-sections"
        data = {}
        if file_input is not None:
            with open(file_input, "rb") as file:
                data["fileInput"] = file
        if fileId is not None:
            data["fileId"] = fileId
        data.update({
            "horizontalDivisions": options.horizontal_divisions,
            "verticalDivisions": options.vertical_divisions,
            "merge": options.merge,
        })
        resp: Response = self.__client.request(
            method="POST", url=url, data=data
        )
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def split_pdf_by_chapters(self, out_path: Path, file_input: Optional[Path] = None, fileId: Optional[str] = None, options: SplitPdfByChaptersOptions = SplitPdfByChaptersOptions()) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        url = "/api/v1/general/split-pdf-by-chapters"
        data = {}
        if file_input is not None:
            with open(file_input, "rb") as file:
                data["fileInput"] = file
        if fileId is not None:
            data["fileId"] = fileId
        data.update({
            "includeMetadata": options.include_metadata,
            "allowDuplicates": options.allow_duplicates,
            "bookmarkLevel": options.bookmark_level,
        })
        resp: Response = self.__client.request(
            method="POST", url=url, data=data
        )
        save_file(resp=resp, out_path=out_path)
        return resp.text