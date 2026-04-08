from requests import get
from src.base_api_adapter import BaseApiAdapter


class APIAdapter(BaseApiAdapter):
    """
    Класс для подключаться к API и получения географические координаты стран
    и информации о самолетах, находящихся в воздушном пространстве этих стран.
    """

    def __init__(self, country) -> None:
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

        response = get(url=self.__openstreetmap_url, params=params_nominatim, headers=headers_nominatim)

        response.raise_for_status()
        print(f"OSM Status: {response.status_code}")

        data = response.json()

        if data:
            self.coordinate = data[0].get('boundingbox')


    def get_airplanes(self) -> None:
        """Метод для получения информации о самолетах, находящихся в воздушном пространстве страны"""

        #Параметры для фильтрации самолетов по их географическим координатам.
        params = {
            'lamin': self.coordinate[0],
            'lamax': self.coordinate[1],
            'lomin': self.coordinate[2],
            'lomax': self.coordinate[3],
        }

        response = get(url=self.__opensky_url, params=params)
        if response.status_code == 200:
            self.aeroplanes = response.json()
            print("Данные о самолетах успешно получены")
        else:
            print(f"Ошибка OpenSky: {response.status_code}")




api = APIAdapter("Canada")
api.get_coordinate()
api.get_airplanes()

