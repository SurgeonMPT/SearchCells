# Импорт библиотек
import sys
from PyQt5.QtWidgets import QApplication
from classes.main_window import MainWindow


# Функция для вывода ошибок, в местах где не выводится
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# Старт программы
if __name__ == '__main__':
    # Прописываем, что нужно выводить ошибку в местах, где не выводится
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    # Создаем ссылки на все окна
    main_window = MainWindow()
    # Открываем главное окно
    main_window.show()
    # Закрытие приложения
    sys.exit(app.exec_())
