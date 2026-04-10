from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseFileConnect(ABC):
    @abstractmethod
    def add_data(self, data: dict) -> None:
        """Добавить запись о самолете в хранилище"""
        pass

    @abstractmethod
    def get_data(self, criteria: Dict[str, Any]) -> List[Any]:
        """Получить данные по критериям (например, по позывному)"""
        pass

    @abstractmethod
    def remove_data(self, criteria: dict) -> None:
        """Удалить данные из хранилища по критериям"""
        pass
