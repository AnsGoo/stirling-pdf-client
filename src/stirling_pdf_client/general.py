
from dataclasses import dataclass, fields
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
        files = {}
        file = None
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if fileId is not None:
            data["fileId"] = fileId
        data.update({
            "horizontalDivisions": options.horizontal_divisions,
            "verticalDivisions": options.vertical_divisions,
            "merge": options.merge,
        })
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def split_pdf_by_chapters(self, out_path: Path, file_input: Optional[Path] = None, fileId: Optional[str] = None, options: SplitPdfByChaptersOptions = SplitPdfByChaptersOptions()) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        url = "/api/v1/general/split-pdf-by-chapters"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if fileId is not None:
            data["fileId"] = fileId
        data.update({
            "includeMetadata": options.include_metadata,
            "allowDuplicates": options.allow_duplicates,
            "bookmarkLevel": options.bookmark_level,
        })
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text
    def split_pages(self, out_path: Path, file_input: Optional[Path] = None, fileId: Optional[str] = None, page_numbers:str = 'all') -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        url = "/api/v1/general/split-pages"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if fileId is not None:
            data["fileId"] = fileId
        data.update({
            "pageNumbers": page_numbers,
        })
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text
    
    def split_by_size_or_count(self, out_path: Path, file_input: Optional[Path] = None, fileId: Optional[str] = None, split_type:Literal['size', 'page','document'] = 'size', split_value:str='10MB') -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        url = "/api/v1/general/split-by-size-or-count"
        SPLIT_TYPE_MAP = {
            'size': 0,
            'page': 1,
            'document': 2,
        }
        data = {
            "splitType": SPLIT_TYPE_MAP[split_type],
            "splitValue": split_value,
        }
        file = None
        files = {}
        if file_input is not None:
            file =  open(file_input, "rb")
            files["fileInput"] = file
        if fileId is not None:
            data["fileId"] = fileId
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text
    
    def scale_page(self, out_path: Path, file_input: Optional[Path] = None, fileId: Optional[str] = None,page_size:Literal['A0','A1','A2','A3','A4','A5','A6','LETTER','LEGAL',"KEEP"] = 'A4', scale_factor:float = 1.0) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        url = "/api/v1/general/scale-page"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file   
        if fileId is not None:
            data["fileId"] = fileId
        data.update({
            "pageSize": page_size,
            "scale": scale_factor,
        })
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text
    
    def rotate_page(self, out_path: Path, file_input: Optional[Path] = None, fileId: Optional[str] = None, angle:Literal[0,90,180,270] = 90) -> str:
        if file_input is None and fileId is None:
            raise ValueError("file_input and fileId must be provided one of")
        url = "/api/v1/general/rotate-page"
        data = {}
        file = None
        files = {}
        if file_input is not None:
            file = open(file_input, "rb")
            files["fileInput"] = file
        if fileId is not None:
            data["fileId"] = fileId
        data.update({
            "angle": angle,
        })
        resp: Response = self.__client.request(
            method="POST", url=url, data=data, files=files
        )
        if file_input is not None:
            file.close()
        save_file(resp=resp, out_path=out_path)
        return resp.text