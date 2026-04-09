import pytest
import os
from src.connect_json import ConnectJson


def test_json_add_and_read(temp_db):
    """Проверяем запись и чтение"""
    data = {"callsign": "TEST_UNIT", "country": "TestLand", "speed": 100, "height": 200}
    temp_db.add_data(data)

    all_records = temp_db._read_all()
    assert len(all_records) == 1
    assert all_records[0]["callsign"] == "TEST_UNIT"


def test_json_get_criteria(temp_db):
    """Проверяем поиск по критериям"""
    temp_db.add_data({"callsign": "PLANE1", "country": "USA"})
    temp_db.add_data({"callsign": "PLANE2", "country": "France"})

    result = temp_db.get_data({"country": "France"})
    assert len(result) == 1
    assert result[0]["callsign"] == "PLANE2"


def test_json_remove(temp_db):
    """Проверяем удаление данных"""
    temp_db.add_data({"callsign": "TO_DELETE", "country": "Any"})
    temp_db.remove_data({"callsign": "TO_DELETE"})

    result = temp_db.get_data({"callsign": "TO_DELETE"})
    assert len(result) == 0