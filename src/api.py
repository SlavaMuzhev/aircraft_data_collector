from requests import get, RequestException
from src.base_api_adapter import BaseApiAdapter


class APIAdapter(BaseApiAdapter):
    """
    Класс для подключаться к API и получения географические координаты стран
    и информации о самолетах, находящихся в воздушном пространстве этих стран.
    """

    def __init__(self, country: str) -> None:
        super().__init__()
        self.__openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.__opensky_url = 'https://opensky-network.org/api/states/all?'
        self.__country = country
        self.__coordinate = None
        self.__aeroplanes = None


    def get_coordinate(self) -> None:
        """Метод для подключенияя к API и получения географических координат стран"""
        #Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        #Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        headers_nominatim = {'User-Agent': 'test-app/1.0'}

        #Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': self.__country,
            'format': 'json',
            'limit': 1,
        }

        try:
            response = self._connect(self.__openstreetmap_url, params_nominatim, headers_nominatim)
            data = response.json()
            if data:
                self.__coordinate = [float(x) for x in data[0].get('boundingbox')]
                print(f"Координаты {self.__country} получены.")
        except RequestException as e:
            print(f"Ошибка при получении координат: {e}")

    def get_airplanes(self) -> None:
        if not self.__coordinate:
            self.get_coordinate()

        if self.__coordinate is None:
            return

        params = {
            'lamin': self.__coordinate[0], 'lamax': self.__coordinate[1],
            'lomin': self.__coordinate[2], 'lomax': self.__coordinate[3],
        }

        try:
            response = self._connect(self.__opensky_url, params)
            self.__aeroplanes = response.json()
            print("Данные о самолетах получены.")
        except RequestException as e:
            print(f"Ошибка при получении данных о самолетах: {e}")

    @property
    def coordinate(self):
        return self.__coordinate

    @property
    def aeroplanes(self):
        return self.__aeroplanes


