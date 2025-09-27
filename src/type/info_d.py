from dataclasses import dataclass
from itertools import count


@dataclass
class Status:
    """表示Stirling PDF服务器状态的类型定义。
    
    属性:
        version: str - 服务器版本号
        status: str - 服务器运行状态
    """
    version: str
    status: str


@dataclass
class LoadCount:
    endpoint: str
    count: int