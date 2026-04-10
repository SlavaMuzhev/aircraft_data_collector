from src.aeroplane import Aeroplane


def test_aeroplane_properties(fast_plane: Aeroplane) -> None:
    """Проверка геттеров"""
    assert fast_plane.callsign == "FAST123"
    assert fast_plane.country == "Canada"
    assert fast_plane.speed == 900.0
    assert fast_plane.height == 10000.0


def test_aeroplane_speed_comparison(fast_plane: Aeroplane, slow_plane: Aeroplane) -> None:
    """Сравнение по скорости через специальный метод (не магический)"""
    assert fast_plane.is_faster_than(slow_plane) is True


def test_aeroplane_height_comparison(fast_plane: Aeroplane, slow_plane: Aeroplane) -> None:
    """Сравнение по высоте через МАГИЧЕСКИЕ методы (по критерию)"""
    assert slow_plane > fast_plane
    assert fast_plane < slow_plane


def test_validation_with_nones() -> None:
    """Проверка приватной валидации"""
    state_with_nones = [None] * 10
    plane = Aeroplane(state_with_nones)
    assert plane.speed == 0.0
    assert plane.callsign == "Unknown"
