from httpx import Response
from pathlib import Path
import re
import urllib.parse


def save_file(resp: Response, out_path: Path):
    target_file = out_path
    if not out_path.is_file():
        filename = get_filename(resp)
        target_file = out_path.joinpath(filename)
    with open(target_file, "wb") as f:
        f.write(resp.content)


def get_filename(resp: Response, default_filename="unkown_filename") -> str:
    """提取文件名的主方法"""
    headers = resp.headers
    content_disposition = headers.get("content-disposition", "")

    # 从Content-Disposition提取
    if content_disposition:
        match = re.search(r"filename\*?=([^;]+)", content_disposition, re.IGNORECASE)
        if match:
            filename = match.group(1).strip(" \"'")
            # 处理编码
            if filename.startswith("UTF-8''") or filename.startswith("utf-8''"):
                filename = urllib.parse.unquote(filename[7:])
            return re.sub(r'[<>:"/\\|?*]', "_", filename)
    return default_filename
