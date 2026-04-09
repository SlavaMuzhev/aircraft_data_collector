import json
import os
from src.base_file_connect import BaseFileConnect


class ConnectJson(BaseFileConnect):
    def __init__(self, filename: str):
        self.file_path = os.path.join('data', filename)

        os.makedirs('data', exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read_all(self) -> list:
        """Метод для чтения данных"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_all(self, data: list):
        """Метод для записи данных"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_data(self, aeroplane_data: dict):
        """Добавление данных о самолете в файл"""
        all_data = self._read_all()
        all_data.append(aeroplane_data)
        self._write_all(all_data)
        print(f"Запись о {aeroplane_data.get('callsign')} добавлена в {self.file_path}")

    def get_data(self, criteria: dict) -> list:
        """Поиск данных по критериям"""
        all_data = self._read_all()
        return [
            item for item in all_data
            if all(item.get(k) == v for k, v in criteria.items())
        ]

    def remove_data(self, criteria: dict):
        """Удаление записей по критериям"""
        all_data = self._read_all()
        new_data = [
            item for item in all_data
            if not all(item.get(k) == v for k, v in criteria.items())
        ]
        self._write_all(new_data)
