from httpx import Client, Response
from typing import Literal, Optional
from pathlib import Path
from .utils import save_file
from .mix import MixApi


class FilterApi(MixApi):
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def filter_page_size(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        standard_page_size: Literal[
            "A0", "A1", "A2", "A3", "A4", "A5", "A6", "LETTER", "LEGAL"
        ] = "A4",
    ) -> str:
        url = "/api/v1/filter/filter-page-size"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["standardPageSize"] = standard_page_size

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def filter_page_rotation(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        rotation: int = 0,
    ) -> str:
        url = "/api/v1/filter/filter-page-rotation"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["rotation"] = rotation

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def filter_page_count(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        page_count: int = 0,
    ) -> str:
        url = "/api/v1/filter/filter-page-count"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["pageCount"] = page_count

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def filter_file_size(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        comparator: Literal["Greater", "Equal", "Less"] = "Greater",
        file_size: int = 0,
    ) -> str:
        url = "/api/v1/filter/filter-file-size"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["fileSize"] = file_size

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def filter_contains_text(
        self,
        out_path: Path,
        text: str,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_numbers: str = "all",
    ) -> str:
        url = "/api/v1/filter/filter-contains-text"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["text"] = text
        data["pageNumbers"] = page_numbers

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text

    def filter_contains_image(
        self,
        out_path: Path,
        file_input: Optional[Path] = None,
        file_id: Optional[str] = None,
        page_numbers: str = "all",
    ) -> str:
        url = "/api/v1/filter/filter-contains-image"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["pageNumbers"] = page_numbers

        resp: Response = self.__client.request(
            method="POST", url=url, files=files, data=data
        )
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text
