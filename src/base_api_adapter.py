from abc import ABC, abstractmethod


class BaseApiAdapter(ABC):
    """
    Абстрактный класс для работы с API сервисов
    для получения географические координаты стран
    и информации о самолетах
    """

    @abstractmethod
    def get_coordinate(self, country: str) -> None:
        pass

    @abstractmethod
    def get_airplanes(self) -> None:
        pass

