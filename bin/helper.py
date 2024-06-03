import os
import json


class Helper:
    """
    Класс помощник с различными функциями
    """

    def __init__(self):
        """
        Инициализация свойств класса
        """
        self.check_settings()
        self.settings = self.get_settings()
        self.languages_list = (("Русский", "ru.json"), ("English", "en.json"))
        self.check_language()

    def write_json(self, file_path, data):
        """
        Запись json файла
        :param file_path: Путь до файла
        :param data: данный для записи
        :return:
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def check_settings(self):
        """
        Проверки наличия файла настроек
        :return:
        """
        file_path = os.path.join('./resources/', 'settings.json')
        if not os.path.exists(file_path):
            data = {
                "language": "ru.json"
            }
            self.write_json(file_path, data)

            print(f"Файл settings.json создан")
        else:
            print(f"Файл settings.json уже существует")

    def get_settings(self):
        """
        Получение настроек программы
        :return: Словарь с настройками
        """
        file_path = os.path.join('./resources/', 'settings.json')

        # Проверяем, что файл существует
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Ошибка при чтении файла settings.json: {e}")
                return {}
        else:
            print(f"Файл settings.json не найден")
            return {}

    def get_language(self, filename='ru.json'):
        """
        Получение языкового словаря
        :param filename: Файл для чтения
        :return: Словарь со словами
        """
        file_path = os.path.join('./resources/languages/', filename)

        # Проверяем, что файл существует
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Ошибка при чтении файла {filename}: {e}")
                return {}
        else:
            print(f"Файл {filename} не найден")
            return {}

    def check_language(self):
        """
        Функция для проверки стандартных файлов со словарями языков
        :return: Ничего не возвращает, проверяет и создает если нет
        """
        directory = './resources/languages/'

        filename = 'ru.json'
        file_path = os.path.join(directory, filename)
        os.remove(file_path)
        if not os.path.exists(file_path):
            data = {
                "info": "Справка",
                "language": "Язык",
                "scanning model": "Модель сканирования",
                "exit": "Выход",
                "cancel": "Отмена",
                "scanning": "Сканирование",
                "setting": "Настройка"
            }
            self.write_json(file_path, data)

            print(f"Файл {filename} создан в {directory}")
        else:
            print(f"Файл {filename} уже существует в {directory}")

        filename = 'en.json'
        file_path = os.path.join(directory, filename)
        os.remove(file_path)
        if not os.path.exists(file_path):
            data = {
                "info": "Info",
                "language": "Language",
                "scanning model": "Scanning model",
                "exit": "Exit",
                "cancel": "Cancel",
                "scanning": "Scanning",
                "setting": "Setting"
            }
            self.write_json(file_path, data)

            print(f"Файл {filename} создан в {directory}")
        else:
            print(f"Файл {filename} уже существует в {directory}")
