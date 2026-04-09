import pytest
from src.base_api_adapter import BaseApiAdapter



def test_base_api_interface():
    class MockApi(BaseApiAdapter):
        def get_coordinate(self, country): return super().get_coordinate(country)

        def get_airplanes(self): return super().get_airplanes()

    api = MockApi()
    api.get_coordinate("test")
    api.get_airplanes()


