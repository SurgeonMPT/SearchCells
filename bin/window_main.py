from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


# Класс главного окна для выбора метода
class MainWindow(QMainWindow):
    # Инициализация свойств класса
    def __init__(self):
        super().__init__()
        self.scan_window = None
        self.initUI()

        # Установка иконки окна
        self.setWindowIcon(QIcon('./resources/images/icon.ico'))

    # Функция для отображения внешнего вида окна
    def initUI(self):
        uic.loadUi('./resources/templates/window_main.ui', self)
