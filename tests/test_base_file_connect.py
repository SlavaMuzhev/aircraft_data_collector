from typing import Any, Dict, List

import pytest

from src.base_file_connect import BaseFileConnect


def test_base_file_connect_interface() -> None:
    """Тестируем наличие методов и корректность вызова super()"""

    class MockFileConnector(BaseFileConnect):
        def add_data(self, data: Dict[str, Any]) -> None:
            super().add_data(data)  # type: ignore[safe-super]

        def get_data(self, criteria: Dict[str, Any]) -> List[Any]:
            return super().get_data(criteria)  # type: ignore[safe-super, return-value]

        def remove_data(self, criteria: Dict[str, Any]) -> None:
            super().remove_data(criteria)  # type: ignore[safe-super]

    connector = MockFileConnector()

    connector.add_data({})
    connector.get_data({})
    connector.remove_data({})


def test_cannot_instantiate_base_class() -> None:
    """Проверяем, что нельзя создать объект абстрактного класса напрямую"""
    with pytest.raises(TypeError):
        BaseFileConnect()  # type: ignore[abstract]
