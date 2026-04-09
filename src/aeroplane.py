class Aeroplane:
    """
    Класс для работы с информацией о самолетах.
    Класс поддерживает методы сравнения самолетов между собой по скорости и высоте,
    валидирует данные, которыми инициализируются его атрибуты
    """

    def __init__(self, state_vector: list) -> None:
        self.callsign = str(state_vector[1]).strip() if state_vector[1] else "Unknown"
        self.country = str(state_vector[2]) if state_vector[2] else "Unknown"

        self.speed = float(state_vector[9]) if state_vector[9] is not None else 0.0
        self.height = float(state_vector[7]) if state_vector[7] is not None else 0.0

    def __lt__(self, other):
        return self.speed < other.speed

    def __le__(self, other):
        return self.speed <= other.speed

    def __gt__(self, other):
        return self.speed > other.speed

    def __ge__(self, other):
        return self.speed >= other.speed

    def __eq__(self, other):
        return self.speed == other.speed


    def compare_height(self, other):
        """Метод для сравнения высоты двух самолетов"""
        if self.height > other.height:
            return f"{self.callsign} летит выше, чем {other.callsign}"
        elif self.height < other.height:
            return f"{self.callsign} летит ниже, чем {other.callsign}"
        return "Высота одинаковая"

    def __repr__(self):
        return f"Plane {self.callsign} ({self.country}): V={self.speed}, H={self.height}"
