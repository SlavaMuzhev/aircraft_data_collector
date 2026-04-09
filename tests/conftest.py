import pytest
import os
from src.aeroplane import Aeroplane
from src.connect_json import ConnectJson


@pytest.fixture
def fast_plane():
    state = [None, "FAST123", "Canada", None, None, None, None, 10000, None, 900]
    return Aeroplane(state)

@pytest.fixture
def slow_plane():
    state = [None, "SLOW456", "France", None, None, None, None, 12000, None, 400]
    return Aeroplane(state)


@pytest.fixture
def temp_db():
    """Создает временный файл в папке data для тестов"""
    test_file = "test_data.json"
    connector = ConnectJson(test_file)
    yield connector
    path = os.path.join('data', test_file)
    if os.path.exists(path):
        os.remove(path)