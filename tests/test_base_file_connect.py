import pytest
from src.base_file_connect import BaseFileConnect


def test_base_file_connect_interface():
    """Тестируем наличие методов и корректность вызова super()"""

    class MockFileConnector(BaseFileConnect):
        def add_data(self, data: dict):
            return super().add_data(data)

        def get_data(self, criteria: dict):
            return super().get_data(criteria)

        def remove_data(self, criteria: dict):
            return super().remove_data(criteria)

    connector = MockFileConnector()

    assert connector.add_data({}) is None
    assert connector.get_data({}) is None
    assert connector.remove_data({}) is None


def test_cannot_instantiate_base_class():
    """Проверяем, что нельзя создать объект абстрактного класса напрямую"""
    with pytest.raises(TypeError):
        BaseFileConnect()