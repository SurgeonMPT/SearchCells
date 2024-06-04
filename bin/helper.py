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
                "language": "ru.json",
                "languages": {
                    "ru.json": "Русский",
                    "en.json": "English",
                }
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
                "ok": "Принять",
                "cancel": "Отмена",
                "scanning": "Сканирование",
                "scan": "Сканировать",
                "setting": "Настройка",
                "next": "Далее",
                "cell": "Клетка",
                "cells": "Клеток",
                "choose": "Выбрать",
                "setting method": "Настройка метода",
                "method parameters": "Параметры метода",
                "parameter k": "Параметр K",
                "size pixel": "Размер на 1 пиксель",
                "Первая попытка": "Первая попытка",
                "Неплоский фон": "Неплоский фон",
                "Фурье": "Фурье",
                "Водораздел": "Водораздел",
                "Водораздел с контурами": "Водораздел с контурами",
                "Водораздел другой формат": "Водораздел другой формат",
                "Гадалка-модель": "Гадалка-модель",
                "Поиск локальный максимумов": "Поиск локальный максимумов",
                "file to scan": "Файл для сканирования",
                "folder to scan": "Папка для сканирования",
                "format to scan": "Формат для сканирования",
                "folder to save": "Папка для сохранения",
                "display final image": "Отображать итоговое изображение",
                "error": "Ошибка",
                "error not found file": "Не выбраны файлы для сканирования",
                "method": "Метод",
                "scan results": "Результаты сканирования",
                "picture": "Картинка",
                "detected": "Обнаружено",
                "choose a picture": "Выбрать картинку",
                "choose a folder": "Выбрать папку",
                "info content": """\tДанное приложение предназначено для определения и выделения клеток на медицинском
изображении.\n \tДля начала работы требуется выбрать метод для определения и отображения клеток. После 
чего требуется выбрать либо файл либо папку для сканирования изображений. Также возможно выбрать папку 
для сохранения итоговых изображений. Если метод требует дополнительных данных, то будет доступна кнопка 
для настроек метода. После настроенных параметров, для выполнении программы требуется нажать на кнопку
сканировать.
\n \tВерсия проекта: 1.0"""
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
                "ok": "Ok",
                "cancel": "Cancel",
                "scanning": "Scanning",
                "scan": "Scan",
                "setting": "Setting",
                "next": "Next",
                "cell": "Cell",
                "cells": "Cells",
                "choose": "Choose",
                "setting method": "Setting method",
                "method parameters": "Method parameters",
                "parameter k": "Parameter k",
                "size pixel": "Size per 1 pixel",
                "Первая попытка": "The first attempt",
                "Неплоский фон": "Non-flat background",
                "Фурье": "Fourier",
                "Водораздел": "Watershed",
                "Водораздел с контурами": "Watershed with contours",
                "Водораздел другой формат": "Watershed is a different format",
                "Гадалка-модель": "The fortune teller is a model",
                "Поиск локальный максимумов": "Search for local highs",
                "file to scan": "File to scan",
                "folder to scan": "Folder to scan",
                "format to scan": "Format to scan",
                "folder to save": "Folder to save",
                "display final image": "Display the final image",
                "error": "Error",
                "method": "Method",
                "scan results": "Scan results",
                "picture": "Picture",
                "detected": "Detected",
                "choose a picture": "Choose a picture",
                "choose a folder": "Choose a folder",
                "error not found file": "No files have been selected for scanning",
                "info content": """\tThis application is designed to identify and isolate cells in a medical
image.\n\tTo get started, you need to select a method for identifying and displaying cells. After
then you need to select either a file or a folder for scanning images. It is also possible to select a folder
to save the final images. If the method requires additional data, the button will be available
for method settings. After the configured parameters, you need to press the button to run the program
scan it.
\n \tProject Version: 1.0"""
            }
            self.write_json(file_path, data)

            print(f"Файл {filename} создан в {directory}")
        else:
            print(f"Файл {filename} уже существует в {directory}")
