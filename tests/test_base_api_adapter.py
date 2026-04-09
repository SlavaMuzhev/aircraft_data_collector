import pytest
from src.base_api_adapter import BaseApiAdapter


def test_base_api_adapter_methods():
    """вызов методов базового класса"""

    class MockApi(BaseApiAdapter):
        def get_coordinate(self, country):
            return BaseApiAdapter.get_coordinate(self, country)

        def get_airplanes(self):
            return BaseApiAdapter.get_airplanes(self)

    mock = MockApi()
    mock.get_coordinate("Any")
    mock.get_airplanes()


