from abc import ABC, abstractmethod
import requests



class BaseApiAdapter(ABC):
    """
    Абстрактный класс для работы с API сервисов
    для получения географические координаты стран
    и информации о самолетах
    """

    @abstractmethod
    def get_coordinate(self, country: str):
        pass

    @abstractmethod
    def get_airplanes(self):
        pass

    def _connect(self, url, params=None, headers=None):
        """
        Реализованный метод подключения.
        Критерий: отправляет запрос на URL и проверяет статус-код.
        """
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Выбросит ошибку, если статус не 200-299
        return response

