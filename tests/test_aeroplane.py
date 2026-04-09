from src.aeroplane import Aeroplane


def test_aeroplane_properties(fast_plane):
    """Проверка инкапсуляции и геттеров"""
    assert fast_plane.callsign == "FAST123"
    assert fast_plane.country == "Canada"
    assert fast_plane.speed == 900.0
    assert fast_plane.height == 10000.0

def test_aeroplane_speed_comparison(fast_plane, slow_plane):
    """Проверка сравнения по скорости (>, <, ==)"""
    assert fast_plane > slow_plane
    assert slow_plane < fast_plane
    assert (fast_plane == slow_plane) is False

def test_aeroplane_height_comparison(fast_plane, slow_plane):
    """Проверка метода сравнения по высоте"""
    assert slow_plane.is_higher_than(fast_plane) is True
    assert fast_plane.is_higher_than(slow_plane) is False

def test_aeroplane_to_dict(fast_plane):
    """Проверка метода подготовки данных для JSON"""
    data = fast_plane.to_dict()
    assert data["callsign"] == "FAST123"
    assert data["speed"] == 900.0
    assert isinstance(data, dict)

def test_validation_with_nones():
    """Проверка валидации, если API прислало None вместо чисел"""
    state_with_nones = [None, None, None, None, None, None, None, None, None, None]
    plane = Aeroplane(state_with_nones)
    assert plane.speed == 0.0
    assert plane.height == 0.0
    assert plane.callsign == "Unknown"