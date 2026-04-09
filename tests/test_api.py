import pytest
from unittest.mock import patch, MagicMock
from requests import exceptions
from requests.exceptions import RequestException
from src.api import APIAdapter


def test_api_adapter_init(api_adapter):
    """Тестируем инициализацию (доступ через манглинг, так как country приватный)"""
    assert api_adapter._APIAdapter__country == "Canada"
    assert api_adapter.coordinate is None
    assert api_adapter.aeroplanes is None


@patch('src.api.APIAdapter._connect')
def test_get_coordinate_success(mock_connect, api_adapter):
    """Тестируем получение координат"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {'boundingbox': ['41.67', '83.33', '-141.00', '-52.32']}
    ]
    mock_connect.return_value = mock_response

    api_adapter.get_coordinate()

    assert api_adapter.coordinate == [41.67, 83.33, -141.00, -52.32]
    assert isinstance(api_adapter.coordinate[0], float)


@patch('src.api.APIAdapter._connect')
def test_get_coordinate_not_found(mock_connect, api_adapter):
    """Тестируем случай, если страна не найдена"""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_connect.return_value = mock_response

    api_adapter.get_coordinate()
    assert api_adapter.coordinate is None


@patch('src.api.APIAdapter._connect')
def test_get_airplanes_success(mock_connect, api_adapter):
    """Тестируем получение самолетов"""
    api_adapter._APIAdapter__coordinate = [40.0, 50.0, -100.0, -90.0]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'states': [['abc', 'FLIGHT1', 'Canada', 0, 0, 0, 0, 10000, False, 250]]
    }
    mock_connect.return_value = mock_response

    api_adapter.get_airplanes()

    assert api_adapter.aeroplanes is not None
    assert api_adapter.aeroplanes['states'][0][1] == 'FLIGHT1'


@patch('src.api.APIAdapter._connect')
def test_get_airplanes_no_coordinates(mock_connect, api_adapter):
    """Тестируем блокировку вызова без координат"""
    mock_connect.return_value.json.return_value = []
    api_adapter.get_airplanes()
    assert api_adapter.aeroplanes is None


@patch('src.api.APIAdapter._connect')
def test_get_coordinate_network_error(mock_connect, api_adapter):
    """Тест ошибки RequestException"""
    mock_connect.side_effect = exceptions.RequestException("Network fail")
    api_adapter.get_coordinate()
    assert api_adapter.coordinate is None


@patch('src.api.APIAdapter._connect')
def test_get_airplanes_error_status(mock_connect, api_adapter):
    """Тест обработки ошибки статуса через Mock"""
    api_adapter._APIAdapter__coordinate = [0, 0, 0, 0]
    mock_connect.side_effect = exceptions.HTTPError("500 Server Error")

    api_adapter.get_airplanes()
    assert api_adapter.aeroplanes is None
