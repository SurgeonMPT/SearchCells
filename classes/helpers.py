# Функция на проверку существования файла
import importlib
import inspect
import os
import sys


# Функция выключения приложения
def exit_app():
    sys.exit(0)


# Функция проверки существования файла
def exist_file(file):
    if os.path.exists(file):
        return file
    else:
        print("Файл не существует")
        return ''


# Функция записи словаря в текстовой файл
def write_dict_file_txt(path, dict_data):
    try:
        with open(f'{path}.txt', mode='wt', encoding='utf-8') as file:
            for index, data in enumerate(dict_data.items()):
                key, value = data
                if index < len(dict_data) - 1:
                    value += '\n'
                file.write(f'{key}---{value}')
        return True
    except Exception as e:
        print(f'Возникла ошибка при записи: {e}')
        return False


# Функция записи словаря в текстовой файл
def read_dict_file_txt(path):
    try:
        with open(f'{path}.txt', mode='rt', encoding='utf-8') as file:
            temp = file.read().split('\n')
            data = {}
            for value in temp:
                value = value.split('---')
                data[value[0]] = value[1]
            return data
    except Exception as e:
        print(f'Возникла ошибка при чтении: {e}')
        return False


# Функция удаления файла
def remove_file(path):
    try:
        os.remove(path)
        return True
    except Exception as e:
        print(f'Возникла ошибка при удалении: {e}')
        return False


# Была идея, чтобы можно было написать программу способную подключать алгоритмы динамически
# как бы сделав возможность добавлять в будущем новые алгоритмы, но это привело к тому, что пришлось бы
# к файлам алгоритмы закидывать используемые библиотеки, что не совсем хорошо и затратно по ресурсам
# поэтому методы снизу реализованы, но не используются больше
# Функция для получения классов в определенной папке
def get_classes(path):
    files = os.listdir(path)
    result_files = []

    # Итерируемся по файлам
    for file in files:
        # Проверяем, что файл имеет расширение .py
        if file.endswith('.py'):
            # Загружаем модуль
            module_name = os.path.splitext(file)[0]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(path, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Извлекаем все атрибуты модуля
            attributes = inspect.getmembers(module)

            # Итерируемся по атрибутам и выводим в консоль только классы с атрибутом name
            for name, attribute in attributes:
                if inspect.isclass(attribute) and hasattr(attribute, 'NAME'):
                    result_files.append({
                        'name': attribute.NAME,
                        'name_class': name,
                        'path': os.path.splitext(file)[0]
                    })
    return result_files


# Импорт класса из указанного файла
def get_import_class(path, name_class):
    # Импорт модуля из указанного пути
    mod = __import__(path, fromlist=[name_class])
    return getattr(mod, name_class)


# Получаем текущий путь
def get_current_path():
    return os.getcwd().replace('\\', '/')
