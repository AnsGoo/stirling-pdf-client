import pytest
from unittest.mock import patch, MagicMock
from src.client import StirlingPDFClient


@pytest.fixture
def client():
    """创建一个StirlingPDFClient实例的fixture"""
    return StirlingPDFClient(base_url="http://localhost:8080")


@patch('src.client.Client')
def test_client_initialization(mock_client_class):
    """测试StirlingPDFClient的初始化是否正确"""
    # 配置mock
    mock_client_instance = MagicMock()
    mock_client_class.return_value = mock_client_instance
    
    # 执行初始化
    base_url = "http://localhost:8080"
    client = StirlingPDFClient(base_url=base_url)
    
    # 验证Client是否被正确调用
    mock_client_class.assert_called_once_with(base_url=base_url)
    # 验证内部client属性是否被正确设置
    assert client._StirlingPDFClient__client == mock_client_instance


@patch('src.client.Client')
def test_get_uptime(mock_client_class, client):
    """测试get_uptime方法是否正确调用API并返回结果"""
    # 配置mock响应
    mock_response = MagicMock()
    expected_result = {"uptime": "10h 30m 15s"}
    mock_response.json.return_value = expected_result
    
    # 配置client的request方法
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.request.return_value = mock_response
    
    # 替换client的内部client属性
    client._StirlingPDFClient__client = mock_client_instance
    
    # 执行get_uptime方法
    result = client.get_uptime()
    
    # 验证request方法是否被正确调用
    mock_client_instance.request.assert_called_once_with(
        method='GET',
        url='api/v1/info/uptime'
    )
    
    # 验证json方法是否被调用
    mock_response.json.assert_called_once()
    
    # 验证返回结果是否正确
    assert result == expected_result


@patch('src.client.Client')
def test_get_uptime_with_different_base_url(mock_client_class):
    """测试使用不同的base_url时的行为"""
    # 配置mock响应
    mock_response = MagicMock()
    mock_response.json.return_value = {"uptime": "5h 15m 30s"}
    
    # 配置client的request方法
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.request.return_value = mock_response
    
    # 使用不同的base_url创建client
    custom_base_url = "http://stirling-pdf.example.com:9090"
    client = StirlingPDFClient(base_url=custom_base_url)
    client._StirlingPDFClient__client = mock_client_instance
    
    # 执行get_uptime方法
    client.get_uptime()
    
    # 验证Client的初始化是否使用了正确的base_url
    mock_client_class.assert_called_once_with(base_url=custom_base_url)
    
    # 验证request方法是否被正确调用，使用了相同的url路径
    mock_client_instance.request.assert_called_once_with(
        method='GET',
        url='api/v1/info/uptime'
    )


@patch('src.client.Client')
def test_get_uptime_handles_empty_response(mock_client_class, client):
    """测试get_uptime方法处理空响应的情况"""
    # 配置mock响应返回空字典
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    
    # 配置client的request方法
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.request.return_value = mock_response
    
    # 替换client的内部client属性
    client._StirlingPDFClient__client = mock_client_instance
    
    # 执行get_uptime方法
    result = client.get_uptime()
    
    # 验证结果是否为空字典
    assert result == {}


@patch('src.client.Client')
def test_get_uptime_handles_request_exception(mock_client_class, client):
    """测试get_uptime方法处理请求异常的情况"""
    # 配置mock抛出异常
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.request.side_effect = Exception("API request failed")
    
    # 替换client的内部client属性
    client._StirlingPDFClient__client = mock_client_instance
    
    # 验证异常是否被正确传播
    with pytest.raises(Exception, match="API request failed"):
        client.get_uptime()