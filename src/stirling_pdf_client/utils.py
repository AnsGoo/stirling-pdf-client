from httpx import Response
from pathlib import Path
import re
from urllib.parse import unquote
from typing import Callable, Any
import functools


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
                filename = unquote(filename[7:])
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


def compare_versions(version1: str, version2: str) -> int:
    """
    比较两个版本号的大小（纯Python实现）。
    
    Args:
        version1: 第一个版本号
        version2: 第二个版本号
        
    Returns:
        -1: 如果version1 < version2
         0: 如果version1 == version2
         1: 如果version1 > version2
    """
    try:
        # 提取数字部分进行比较
        v1_parts = [int(part) for part in re.findall(r'\d+', version1)]
        v2_parts = [int(part) for part in re.findall(r'\d+', version2)]
        
        # 比较每个部分
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1 = v1_parts[i] if i < len(v1_parts) else 0
            v2 = v2_parts[i] if i < len(v2_parts) else 0
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        return 0
    except Exception as e:
        print(f"版本比较错误: {e}")
        # 如果无法解析，返回0表示相等
        return 0


def requires_server_version(min_version: str) -> Callable:
    """版本检查装饰器，确保方法在服务器版本大于等于指定版本时才能调用。
    
    Args:
        min_version: 所需的最小服务器版本
        
    Returns:
        装饰后的函数
    """
    
    def decorator(func: Callable) -> Callable:
        
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            
            # 检查get_client方法
            if not hasattr(self, 'get_client'):
                raise AttributeError("API Object not has get_client function")
            
            try:
                client = self.get_client()
                
                if not hasattr(client, 'version') and hasattr(client, 'server_status'):
                    client.version = client.server_status.get('version', '0.0.0')
                
                # 检查服务器版本
                server_version = getattr(client, 'version', '0.0.0')
                
                # 比较版本
                comparison_result = compare_versions(server_version, min_version)
                
                # 如果版本不满足要求，抛出异常
                if comparison_result < 0:
                    error_msg = f"在当前服务器版本({server_version})下不支持该方法，需要版本 >= {min_version}"
                    raise Exception(error_msg)
                
                # 版本满足要求，调用原函数
                func_result = func(self, *args, **kwargs)
                return func_result
            except Exception as e:
                # 重新抛出异常
                raise e
        return wrapper
    
    return decorator
