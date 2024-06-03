from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """
    Класс главного окна для выбора метода
    """

    def __init__(self, helper):
        """
        Инициализация свойств класса
        """
        super().__init__()
        self.scan_window = None
        self.helper = helper
        self.initUI()

        # Установка иконки окна
        self.setWindowIcon(QIcon('./resources/images/icon.ico'))

        self.languageComboBox.addItems([i[0] for i in self.helper.languages_list])
        language_index = -1
        for index, i in enumerate(self.helper.languages_list):
            if i[1] == self.helper.settings['language']:
                language_index = index
        self.languageComboBox.setCurrentIndex(language_index if language_index != -1 else 0)
        self.languageComboBox.currentIndexChanged.connect(self.on_language_changed)

        self.algComboBox.addItems(["Первая попытка"])
        self.algComboBox.setCurrentIndex(0)

        self.set_language(self.helper.settings["language"])

        self.exitButton.clicked.connect(self.exit_application)

    def initUI(self):
        """
        Функция для отображения внешнего вида окна
        :return: Нет
        """
        uic.loadUi('./resources/templates/window_main.ui', self)

    def on_language_changed(self, index):
        """
        Смена локализации
        :param index:
        :return:
        """
        self.set_language(self.helper.languages_list[index][1])
        self.helper.settings["language"] = self.helper.languages_list[index][1]
        self.helper.write_json("./resources/settings.json", self.helper.settings)

    def set_language(self, language):
        """
        Установка локализации текста
        :param language: Файл с локализацией
        :return:
        """
        for key, value in self.helper.get_language(language).items():
            if key == "language":
                self.languageLabel.setText(value + ":")

            if key == "info":
                self.infoButton.setText(value)

            if key == "scanning model":
                self.modelLabel.setText(value + ":")

            if key == "exit":
                self.exitButton.setText(value)

            if key == "scanning":
                self.scanButton.setText(value)

            if key == "setting":
                self.setWindowTitle(value)

    def exit_application(self):
        """
        Функция для закрытия окна
        :return:
        """
        self.close()
