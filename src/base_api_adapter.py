from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests


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

    def _connect(
        self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Реализованный метод подключения.
        Критерий: отправляет запрос на URL и проверяет статус-код.
        """
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Выбросит ошибку, если статус не 200-299
        return response
