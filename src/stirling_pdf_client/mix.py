from httpx import Client


class MixApi:
    def get_client(self) -> Client:
        """
        获取客户端对象，处理Python名称修饰问题。

        尝试多种可能的客户端属性名称，包括：
        1. 直接查找名称修饰后的客户端属性
        2. 检查是否有_client属性
        3. 检查是否有client属性

        Returns:
            Client: 客户端对象

        Raises:
            AttributeError: 如果找不到客户端对象
        """
        # 尝试直接获取客户端（处理名称修饰问题）
        # 检查实例的所有属性
        for attr_name in self.__dict__:
            # 查找可能的客户端属性名称
            if "client" in attr_name.lower():
                return getattr(self, attr_name)

        # 如果没有找到客户端对象，抛出异常
        raise AttributeError(f"在 {self.__class__.__name__} 实例中找不到客户端对象")
