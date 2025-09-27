
from pathlib import Path
import sys
import os

# 将当前项目根目录添加到Python路径，以便可以直接运行而不需要安装包
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 尝试从已安装的包导入，如果失败则从源码导入
try:
    from stirling_pdf_client import StirlingPDFClient
    print("从已安装的包导入成功")
except ImportError:
    # 如果包尚未安装，则从源码导入
    print("提示: 包'stirling_pdf_client'尚未安装在当前Python环境中。正在从源码导入...")
    print("建议: 运行 'pip install .' 来安装这个包")
    from src.client import StirlingPDFClient

def debug_info():
    # 初始化客户端，指向您的Stirling PDF服务器
    client = StirlingPDFClient(base_url='http://192.168.124.18:18080')
    
    try:
        # 获取服务器运行时间信息
        uptime_info = client.info.get_uptime()
        print(f"服务器运行时间: {uptime_info}")
        status = client.info.get_status()
        print(f"服务器状态:{status}")
        load = client.info.get_load()
        print(f"服务器载荷:{load}")
        load_unique = client.info.get_load_unique()
        print(f"服务器单一API载荷:{load_unique}")
        load_all = client.info.get_load_all()
        print(f"服务器所有API载荷:{load_all}")
        load_all_unique = client.info.get_load_all_unique()
        print(f"服务器所有API载荷:{load_all_unique}")
    except Exception as e:
        print(f"请求失败: {e}")
        print("提示: 请确保Stirling PDF服务器正在运行，并且URL正确")


def main():
    client = StirlingPDFClient(base_url='http://192.168.124.18:18080')
    resp = client.convert.pdf_to_word(file_input=Path('./test.pdf'),out_path=Path('./'))
    print(resp)
    client.convert.pdf_to_text(file_input=Path('./test.pdf'),out_path=Path('./'),output_format='txt')

if __name__ == "__main__":
    main()
