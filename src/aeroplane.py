class Aeroplane:
    """
    Класс для работы с информацией о самолетах.
    Класс поддерживает методы сравнения самолетов между собой по скорости и высоте,
    валидирует данные, которыми инициализируются его атрибуты
    """

    def __init__(self, state_vector: list) -> None:
        self.__callsign = str(state_vector[1]).strip() if state_vector[1] else "Unknown"
        self.__country = str(state_vector[2]) if state_vector[2] else "Unknown"
        self.__speed = float(state_vector[9]) if state_vector[9] is not None else 0.0
        self.__height = float(state_vector[7]) if state_vector[7] is not None else 0.0

    @property
    def callsign(self): return self.__callsign

    @property
    def country(self): return self.__country

    @property
    def speed(self): return self.__speed

    @property
    def height(self): return self.__height

    # Сравнение по скорости
    def __lt__(self, other): return self.speed < other.speed

    def __le__(self, other): return self.speed <= other.speed

    def __gt__(self, other): return self.speed > other.speed

    def __ge__(self, other): return self.speed >= other.speed

    def __eq__(self, other): return self.speed == other.speed

    # Сравнение по высоте
    def is_higher_than(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.height > other.height

    def to_dict(self):
        """Метод для удобного сохранения в JSON через коннектор"""
        return {
            "callsign": self.callsign,
            "country": self.country,
            "speed": self.speed,
            "height": self.height
        }

    def __repr__(self):
        return f"Plane {self.callsign} ({self.country}): V={self.speed}, H={self.height}"
