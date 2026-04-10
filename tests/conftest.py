import os
from typing import Generator

import pytest

from src.aeroplane import Aeroplane
from src.api import APIAdapter
from src.connect_json import ConnectJson


@pytest.fixture
def fast_plane() -> Aeroplane:
    state = [None, "FAST123", "Canada", None, None, None, None, 10000, None, 900]
    return Aeroplane(state)


@pytest.fixture
def slow_plane() -> Aeroplane:
    state = [None, "SLOW456", "France", None, None, None, None, 12000, None, 400]
    return Aeroplane(state)


@pytest.fixture
def temp_db() -> Generator[ConnectJson, None, None]:
    """Создает временный файл в папке data для тестов"""
    test_file = "test_data.json"
    connector = ConnectJson(test_file)
    yield connector
    path = os.path.join("data", test_file)
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def api_adapter() -> APIAdapter:
    """Создает экземпляр APIAdapter для каждого теста"""
    return APIAdapter("Canada")
