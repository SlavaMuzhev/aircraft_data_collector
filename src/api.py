from requests import get, RequestException
from src.base_api_adapter import BaseApiAdapter


class APIAdapter(BaseApiAdapter):
    """
    Класс для подключаться к API и получения географические координаты стран
    и информации о самолетах, находящихся в воздушном пространстве этих стран.
    """

    def __init__(self, country: str) -> None:
        self.__openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.__opensky_url = 'https://opensky-network.org/api/states/all?'
        self.aeroplanes = None
        self.coordinate = None
        self.country = country

    def get_coordinate(self) -> None:
        """Метод для подключенияя к API и получения географических координат стран"""
        #Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        #Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

        #Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': self.country,
            'format': 'json',
            'limit': 1,
        }

        try:
            response = get(url=self.__openstreetmap_url, params=params_nominatim, headers=headers_nominatim, timeout=10)
            response.raise_for_status()

            data = response.json()
            if not data:
                print(f"Ошибка: Страна '{self.country}' не найдена в OSM.")
                return

            self.coordinate = [float(x) for x in data[0].get('boundingbox')]
            print(f"Координаты {self.country} получены: {self.coordinate}")

        except RequestException as e:
            print(f"Ошибка сети при запросе к OSM: {e}")
        except (ValueError, IndexError) as e:
            print(f"Ошибка обработки данных OSM: {e}")


    def get_airplanes(self) -> None:
        """Метод для получения информации о самолетах, находящихся в воздушном пространстве страны"""
        if not self.coordinate:
            print("Ошибка: Нельзя получить самолеты без координат страны.")
            return
        #Параметры для фильтрации самолетов по их географическим координатам.
        params = {
            'lamin': self.coordinate[0],
            'lamax': self.coordinate[1],
            'lomin': self.coordinate[2],
            'lomax': self.coordinate[3],
        }

        try:
            response = get(url=self.__opensky_url, params=params, timeout=15)

            if response.status_code == 200:
                self.aeroplanes = response.json()
                # Проверяем, есть ли поле 'states' (список самолетов)
                flights_count = len(self.aeroplanes.get('states') or [])
                print(f"Данные получены. Найдено самолетов: {flights_count}")
            elif response.status_code == 404:
                print("OpenSky: В указанной области сейчас нет активных самолетов.")
            else:
                print(f"Ошибка OpenSky (Статус {response.status_code}): {response.text}")

        except RequestException as e:
            print(f"Ошибка сети при запросе к OpenSky: {e}")


