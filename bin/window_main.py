from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from bin.methods.scanning_algorithm_v0 import ScanningAlgorithmV0
from bin.methods.scanning_algorithm_v1 import ScanningAlgorithmV1
from bin.methods.scanning_algorithm_v2 import ScanningAlgorithmV2
from bin.methods.scanning_algorithm_v3 import ScanningAlgorithmV3
from bin.methods.scanning_algorithm_v3_1 import ScanningAlgorithmV31
from bin.methods.scanning_algorithm_v3_2 import ScanningAlgorithmV32
from bin.methods.scanning_algorithm_v4 import ScanningAlgorithmV4
from bin.methods.scanning_algorithm_v5 import ScanningAlgorithmV5
from bin.window_method_base import WindowMethodBase
from bin.window_info import WindowInfo


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
        self.info_window = None
        self.helper = helper
        self.methods = [ScanningAlgorithmV0, ScanningAlgorithmV1, ScanningAlgorithmV2, ScanningAlgorithmV3,
                        ScanningAlgorithmV31, ScanningAlgorithmV32, ScanningAlgorithmV4, ScanningAlgorithmV5]
        self.initUI()

    def initUI(self):
        """
        Функция для отображения внешнего вида окна
        :return: Нет
        """
        uic.loadUi('./resources/templates/window_main.ui', self)

        # Установка иконки окна
        self.setWindowIcon(QIcon('./resources/images/icon.ico'))

        self.languageComboBox.addItems([value for key, value in self.helper.settings["languages"].items()])
        language_index = -1
        i = -1
        for key, value in self.helper.settings["languages"].items():
            i += 1
            if key == self.helper.settings['language']:
                language_index = i
        self.languageComboBox.setCurrentIndex(language_index if language_index != -1 else 0)
        self.languageComboBox.currentIndexChanged.connect(self.on_language_changed)

        self.set_language(self.helper.settings["language"])

        self.infoButton.clicked.connect(self.info)
        self.nextButton.clicked.connect(self.next)
        self.exitButton.clicked.connect(self.exit_application)

    def info(self):
        """
        Открытие диалогового окна
        :return:
        """
        self.info_window = WindowInfo(self.helper, self)
        self.info_window.show()
        self.hide()

    def next(self):
        """
        Открытие окна для сканирования клеток
        :return:
        """
        if self.algComboBox.currentIndex() < 0:
            QMessageBox.about(self, 'Ошибка', f'Не выбран алгоритм для сканирования')
        else:
            self.scan_window = WindowMethodBase(self.helper, self, self.methods[self.algComboBox.currentIndex()])
            self.scan_window.show()
            self.hide()

    def on_language_changed(self, index):
        """
        Смена локализации
        :param index:
        :return:
        """
        language = None
        for key, value in self.helper.settings["languages"].items():
            if value == self.languageComboBox.currentText():
                self.set_language(key)
                self.helper.settings["language"] = key
                self.helper.write_json("./resources/settings.json", self.helper.settings)

    def set_language(self, language):
        """
        Установка локализации текста
        :param language: Файл с локализацией
        :return:
        """
        temp = self.helper.get_language(language)
        self.algComboBox.clear()
        self.algComboBox.addItems([temp.get(method.NAME, method.NAME) for method in self.methods])
        self.algComboBox.setCurrentIndex(0)

        for key, value in temp.items():
            if key == "language":
                self.languageLabel.setText(value + ":")

            if key == "info":
                self.infoButton.setText(value)

            if key == "scanning model":
                self.modelLabel.setText(value + ":")

            if key == "exit":
                self.exitButton.setText(value)

            if key == "next":
                self.nextButton.setText(value)

            if key == "setting":
                self.setWindowTitle(value)

    def next(self):
        """
        Открытие окна для сканирования клеток
        :return:
        """
        if self.algComboBox.currentIndex() < 0:
            QMessageBox.about(self, 'Ошибка', f'Не выбран алгоритм для сканирования')
        else:
            self.scan_window = WindowMethodBase(self.helper, self, self.methods[self.algComboBox.currentIndex()])
            self.scan_window.show()
            self.hide()

    def exit_application(self):
        """
        Функция для закрытия окна
        :return:
        """
        self.close()
