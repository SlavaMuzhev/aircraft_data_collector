from abc import ABC, abstractmethod


class BaseFileConnect(ABC):
    @abstractmethod
    def add_data(self, data: dict):
        """Добавить запись о самолете в хранилище"""
        pass

    @abstractmethod
    def get_data(self, criteria: dict):
        """Получить данные по критериям (например, по позывному)"""
        pass

    @abstractmethod
    def remove_data(self, criteria: dict):
        """Удалить данные из хранилища по критериям"""
        pass