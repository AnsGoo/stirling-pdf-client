from httpx import Client, Response
from typing import List, Literal, Optional
from pathlib import Path
from dataclasses import dataclass
from utils import save_file


class FilterApi:
    __client: Client

    def __init__(self, client: Client) -> None:
        self.__client = client

    def filter_page_size(self,out_path:Path, file_input: Optional[Path] = None, file_id: Optional[str] = None, comparator: Literal["Greater", "Equal","Less"] = "Greater",standard_page_size:Literal['A0','A1','A2','A3','A4','A5','A6','LETTER','LEGAL'] = 'A4') -> str:
        url = "/api/filter/pageSize"
        files = {}
        if file_input is not None:
            files["fileInput"] = open(file_input, "rb")
        data = {}
        if file_id is not None:
            data["fileId"] = file_id
        data["comparator"] = comparator
        data["standardPageSize"] = standard_page_size

        resp: Response = self.__client.request(method="POST", url=url, files=files, data=data)
        if file_input is not None:
            files["fileInput"].close()
        save_file(resp=resp, out_path=out_path)
        return resp.text