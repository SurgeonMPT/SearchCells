# Импорт библиотек
import sys
from PyQt5.QtWidgets import QApplication
from bin.window_main import MainWindow
from bin.helper import Helper


def except_hook(cls, exception, traceback):
    """
    Функция для вывода ошибок, в местах где не выводится
    :param cls:
    :param exception:
    :param traceback:
    :return:
    """
    sys.__excepthook__(cls, exception, traceback)


# Старт программы
if __name__ == '__main__':
    # Прописываем, что нужно выводить ошибку в местах, где не выводится
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    # Класс помощника
    helper = Helper()
    # Создаем ссылки на все окна
    main_window = MainWindow(helper)
    # Открываем главное окно
    main_window.show()
    # Закрытие приложения
    sys.exit(app.exec_())
