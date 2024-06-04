from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class WindowInfo(QMainWindow):
    """
    Класс главного окна для выбора метода
    """

    def __init__(self, helper, main_window):
        """
        Инициализация свойств класса
        """
        super().__init__()
        self.helper = helper
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        """
        Функция для отображения внешнего вида окна
        :return: Нет
        """
        uic.loadUi('./resources/templates/window_info.ui', self)

        self.setWindowIcon(QIcon('./resources/images/icon.ico'))
        self.set_language(self.helper.settings["language"])

        self.exitButton.clicked.connect(self.close_window)

    def set_language(self, language):
        """
        Установка локализации текста
        :param language: Файл с локализацией
        :return:
        """
        for key, value in self.helper.get_language(language).items():
            if key == "exit":
                self.exitButton.setText(value)

            if key == "info":
                self.setWindowTitle(value)

            if key == "info content":
                self.infoPlainTextEdit.setPlainText(value)

    def close_window(self):
        """
        Функция для закрытия окна
        :return:
        """
        self.main_window.show()
        self.close()
