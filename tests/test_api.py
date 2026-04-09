from unittest.mock import patch, MagicMock
from requests import exceptions
from requests.exceptions import RequestException
from src.api import APIAdapter


def test_api_adapter_init():
    """Тестируем инициализацию"""
    api = APIAdapter("Canada")
    assert api.country == "Canada"
    assert api.coordinate is None
    assert api.aeroplanes is None

@patch('src.api.get')
def test_get_coordinate_success(mock_get):
    """Тестируем получение координат (Nominatim)"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {'boundingbox': ['41.67', '83.33', '-141.00', '-52.32']}
    ]
    mock_get.return_value = mock_response

    api = APIAdapter("Canada")
    api.get_coordinate()

    assert api.coordinate == [41.67, 83.33, -141.00, -52.32]
    assert isinstance(api.coordinate[0], float)


@patch('src.api.get')
def test_get_coordinate_not_found(mock_get):
    """Тестируем случай, если страна не найдена"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [] # Пустой ответ
    mock_get.return_value = mock_response

    api = APIAdapter("NonExistentCountry")
    api.get_coordinate()

    assert api.coordinate is None

@patch('src.api.get')
def test_get_airplanes_success(mock_get):
    """Тестируем получение самолетов (OpenSky)"""
    api = APIAdapter("Canada")
    api.coordinate = [40.0, 50.0, -100.0, -90.0] # Представим, что координаты уже есть

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'states': [['abc', 'FLIGHT1', 'Canada', 17000, 17000, 0, 0, 10000, False, 250]]
    }
    mock_get.return_value = mock_response

    api.get_airplanes()

    assert api.aeroplanes is not None
    assert len(api.aeroplanes['states']) == 1
    assert api.aeroplanes['states'][0][1] == 'FLIGHT1'


def test_get_airplanes_no_coordinates():
    """Тестируем ошибку, если координаты еще не получены"""
    api = APIAdapter("Canada")
    api.get_airplanes()
    assert api.aeroplanes is None


@patch('src.api.get')
def test_get_coordinate_network_error(mock_get, api_adapter):
    """Тест ошибки сети при запросе координат"""
    mock_get.side_effect = exceptions.RequestException("Network fail")
    api_adapter.get_coordinate()
    assert api_adapter.coordinate is None


@patch('src.api.get')
def test_get_airplanes_http_error(mock_get, api_adapter):
    """Тест HTTP ошибки (например, 500) от OpenSky"""
    api_adapter.coordinate = [40, 50, -100, -90]
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response

    api_adapter.get_airplanes()
    assert api_adapter.aeroplanes is None

@patch('src.api.get')
def test_get_coordinate_exception(mock_get, api_adapter):
    """Имитируем отсутствие интернета"""
    mock_get.side_effect = RequestException("No internet")
    api_adapter.get_coordinate()
    assert api_adapter.coordinate is None

@patch('src.api.get')
def test_get_airplanes_error_status(mock_get, api_adapter):
    """Имитируем ошибку сервера 500"""
    api_adapter.coordinate = [0,0,0,0]
    mock_get.return_value.status_code = 500
    api_adapter.get_airplanes()
