from pathlib import Path

# 尝试从已安装的包导入，如果失败则从源码导入
from stirling_pdf_client import StirlingPDFClient


def debug_info():
    # 初始化客户端，指向您的Stirling PDF服务器
    client = StirlingPDFClient(base_url="http://192.168.124.18:18080")

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


def convert():
    client = StirlingPDFClient(base_url="http://192.168.124.18:18080")
    client.convert.pdf_to_word(
        file_input=Path("./mock/test.pdf"), out_path=Path("./mock")
    )
    client.convert.pdf_to_text(
        file_input=Path("./mock/test.pdf"), out_path=Path("./mock"), output_format="txt"
    )
    client.convert.pdf_to_markdown(
        out_path=Path("./mock"), file_input=Path("./mock/test.pdf")
    )
    client.convert.pdf_to_pdfa(
        out_path=Path("./mock"), file_input=Path("./mock/test.pdf")
    )
    client.convert.pdf_to_presentation(
        out_path=Path("./mock"), file_input=Path("./mock/test.pdf")
    )
    client.convert.pdf_to_img(
        out_path=Path("./mock"), file_input=Path("./mock/test.pdf")
    )


def main():
    debug_info()
    # convert()


if __name__ == "__main__":
    main()
