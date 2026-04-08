class Aeroplane:
    """
    Класс для работы с информацией о самолетах.
    Класс поддерживает методы сравнения самолетов между собой по скорости и высоте,
    валидирует данные, которыми инициализируются его атрибуты
    """

    def __init__(self, data) -> None:
        self.data = data
        self.__validate()

    def __validate(self):
        aeroplane = self.data["states"][0][0]
        self.country_checkin = aeroplane[2]
        self.board_name = aeroplane[1]
        self.speed_fly = aeroplane[9] if aeroplane[8] == "false" else 0
        self.height_fly = aeroplane[7] if aeroplane[8] == "false" else 0

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass