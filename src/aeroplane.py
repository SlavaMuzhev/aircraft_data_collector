from typing import Any, Dict, List, Union


class Aeroplane:
    """
    Класс для работы с информацией о самолетах.
    Класс поддерживает методы сравнения самолетов между собой по скорости и высоте,
    валидирует данные, которыми инициализируются его атрибуты
    """

    __slots__ = ("__callsign", "__country", "__speed", "__height")

    def __init__(self, state_vector: List[Any]) -> None:
        self.__callsign = self.__validate_str(state_vector[1], "Unknown").strip()
        self.__country = self.__validate_str(state_vector[2], "Unknown")
        self.__speed = self.__validate_num(state_vector[9])
        self.__height = self.__validate_num(state_vector[7])

    def __validate_str(self, value: Any, default: str) -> str:
        return str(value) if value else default

    def __validate_num(self, value: Any) -> float:
        try:
            return float(value) if value is not None else 0.0
        except ValueError, TypeError:
            return 0.0

    @property
    def callsign(self) -> str:
        return self.__callsign

    @property
    def country(self) -> str:
        return self.__country

    @property
    def speed(self) -> float:
        return self.__speed

    @property
    def height(self) -> float:
        return self.__height

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__height < other.height

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__height > other.height

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return False
        return self.__height == other.height

    def is_faster_than(self, other: Any) -> Any:
        """Сравнение ПО скорости"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__speed > other.speed

    def to_dict(self) -> Dict[str, Union[str, float]]:
        """Метод для сохранения в JSON (используем приватные атрибуты из __slots__)"""
        return {"callsign": self.__callsign, "country": self.__country, "speed": self.__speed, "height": self.__height}

    def __repr__(self) -> str:
        return f"Plane {self.__callsign}: V={self.__speed}, H={self.__height}"
