import json
import os
from typing import Any, Dict, List

from src.base_file_connect import BaseFileConnect


class ConnectJson(BaseFileConnect):
    def __init__(self, filename: str = "airplanes.json") -> None:
        self.__file_path = os.path.join("data", filename)
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.__file_path):
            self._write_all([])

    def _read_all(self) -> List[Any]:
        """Метод для чтения данных"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError, FileNotFoundError:
            return []

    def _write_all(self, data: list) -> None:
        """Метод для записи данных"""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_data(self, aeroplane_data: dict) -> None:
        """Добавление данных о самолете в файл"""
        all_data = self._read_all()

        if any(item.get("callsign") == aeroplane_data.get("callsign") for item in all_data):
            print(f"Самолет {aeroplane_data.get('callsign')} уже есть в базе.")
            return

        all_data.append(aeroplane_data)
        self._write_all(all_data)
        print(f"Запись о {aeroplane_data.get('callsign')} добавлена.")

    def get_data(self, criteria: Dict[str, Any]) -> list:
        """Поиск данных по критериям (реализован в классе-наследнике)"""
        all_data = self._read_all()
        return [item for item in all_data if all(item.get(k) == v for k, v in criteria.items())]

    def remove_data(self, criteria: Dict[str, Any]) -> None:
        """Удаление записей по критериям (реализован в классе-наследнике)"""
        all_data = self._read_all()
        new_data = [item for item in all_data if not all(item.get(k) == v for k, v in criteria.items())]

        self._write_all(new_data)
