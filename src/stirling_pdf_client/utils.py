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


def validate_response(resp: Response) -> Response:
    """验证HTTP响应状态码，成功时返回响应对象，失败时抛出异常。"""
    # 成功状态码直接返回响应对象
    if 200 <= resp.status_code < 300:
        return resp
        
    # 状态码到错误消息的映射
    error_messages = {
        400: "Bad request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not found",
        405: "Method not allowed",
        413: "Payload too large",
        422: "Unprocessable entity",
        500: "Internal server error",
        502: "Bad gateway",
        503: "Service unavailable",
        504: "Gateway timeout"
    }
    
    # 获取对应的错误消息，如果没有预定义则使用通用消息
    error_msg = error_messages.get(resp.status_code, f"Request failed with status code {resp.status_code}")
    raise Exception(f"{error_msg}: {resp.text}")
