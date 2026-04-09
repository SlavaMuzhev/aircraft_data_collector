from src.api import APIAdapter
from src.aeroplane import Aeroplane
from src.connect_json import ConnectJson


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    Возможности функции:
    1.Ввод названия страны для запроса информации о самолетах из opensky-network.org.
    2.Получение топ N самолетов по высоте полета.
    3.Получение самолетов по стране их регистрации.
    """
    print("--- Система мониторинга воздушного пространства ---")

    connector = ConnectJson("airplanes.json")

    while True:
        print("\nДоступные действия:")
        print("1. Загрузить данные о самолетах для конкретной страны")
        print("2. Показать ТОП-N самых высоких полетов (из файла)")
        print("3. Найти самолеты по стране регистрации (из файла)")
        print("4. Очистить все данные")
        print("0. Выход")

        choice = input("\nВыберите пункт меню: ")

        if choice == "1":
            country_name = input("Введите название страны (на английском, например, Canada): ")
            api = APIAdapter(country_name)

            print(f"Запрашиваем координаты для {country_name}...")
            api.get_coordinate()

            if api.coordinate:
                api.get_airplanes()
                states = api.aeroplanes.get('states') if api.aeroplanes else None

                if states:
                    for state in states:
                        plane = Aeroplane(state)
                        connector.add_data(plane.to_dict())
                    print(f"Успешно обработано {len(states)} самолетов.")
                else:
                    print("В этой области сейчас нет активных самолетов.")

        elif choice == "2":
            try:
                n = int(input("Сколько самолетов вывести в ТОП? "))
            except ValueError:
                print("Ошибка: введите число.")
                continue

            all_planes_data = connector._read_all()

            if not all_planes_data:
                print("Файл пуст. Сначала загрузите данные (пункт 1).")
                continue

            top_planes = sorted(
                all_planes_data,
                key=lambda x: x.get('height', 0) if x.get('height') is not None else 0,
                reverse=True
            )[:n]

            print(f"\n--- ТОП {len(top_planes)} по высоте ---")
            for i, p in enumerate(top_planes, 1):
                callsign = p.get('callsign', 'Unknown')
                height = p.get('height', 0)
                country = p.get('country', 'Unknown')
                print(f"{i}. {callsign} | Высота: {height} м | Страна: {country}")

        elif choice == "3":
            reg_country = input("Введите страну регистрации (например, United States): ")
            results = connector.get_data({'country': reg_country})

            if results:
                for p in results:
                    print(f"Позывной: {p.get('callsign')}, Скорость: {p.get('speed')} км/ч")
            else:
                print("Ничего не найдено.")

        elif choice == "4":
            confirm = input("Вы уверены, что хотите очистить файл? (y/n): ")
            if confirm.lower() == 'y':
                connector._write_all([])
                print("Данные удалены.")

        elif choice == "0":
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    user_interaction()