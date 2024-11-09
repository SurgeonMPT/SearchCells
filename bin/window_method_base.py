import os

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox


class WindowMethodBase(QMainWindow):
    """
    Класс главного окна для выбора метода
    """

    def __init__(self, helper, main_window, method):
        """
        Инициализация свойств класса
        """
        super().__init__()
        self.main_window = main_window
        self.helper = helper
        self.method = method()
        self.language = self.helper.get_language(self.helper.settings['language'])
        self.formats_file = ["*.tif"]
        self.initUI()

    def initUI(self):
        """
        Функция для отображения внешнего вида окна
        :return: Нет
        """
        uic.loadUi('./resources/templates/window_method_base.ui', self)

        self.setWindowIcon(QIcon('./resources/images/icon.ico'))
        self.set_language(self.helper.settings["language"])

        if self.method.dialogParams:
            self.settingsMethodsPushButton.clicked.connect(self.open_dialog_params)
            self.method.dialogParams.set_language(self.helper.get_language(self.helper.settings["language"]))
        else:
            self.settingsMethodsPushButton.hide()

        self.formatToScanComboBox.addItems([i for i in self.formats_file])
        self.formatToScanComboBox.setCurrentIndex(0)

        self.scanButton.clicked.connect(self.scan)
        self.chooseFileToScanPushButton.clicked.connect(self.choose_image)
        self.chooseFolderToScanPushButton.clicked.connect(self.choose_folder_to_scan)
        self.chooseScanToFolderPushButton.clicked.connect(self.choose_folder_to_save)
        self.cancelButton.clicked.connect(self.cancel)
        self.exitButton.clicked.connect(self.exit_application)

    def scan(self):
        """
        Функция запускающая сканирование
        :return:
        """
        if os.path.exists(self.fileToScanLineEdit.text()) or os.path.isdir(self.folderToScanLineEdit.text()):
            data_params = dict()

            data_params['language'] = self.helper.get_language(self.helper.settings["language"])
            if self.method.dialogParams:
                data_params['dop_params'] = self.method.dialogParams.params

            data_params['folder_to_save'] = self.scanToFolderLineEdit.text()
            data_params['show_image'] = self.displayFinalImageCheckBox.isChecked()

            if os.path.isdir(self.folderToScanLineEdit.text()):
                files = []
                for filename in os.listdir(self.folderToScanLineEdit.text()):
                    if (os.path.isfile(os.path.join(self.folderToScanLineEdit.text(), filename)) and
                            filename.endswith(self.formatToScanComboBox.currentText()[1:])):
                        files.append(os.path.join(self.folderToScanLineEdit.text(), filename))

                for i in files:
                    data_params['file_to_scan'] = i
                    result = self.method.scan(data_params)
                    QMessageBox.about(self, self.language["scan results"], f'{self.language["detected"]} '
                                                                           f'"{result["contour_set"]}" '
                                                                           f'{self.language["cells"].lower()}.')
            else:
                data_params['file_to_scan'] = self.fileToScanLineEdit.text()
                result = self.method.scan(data_params)
                QMessageBox.about(self, self.language['scan results'], f'{self.language["detected"]} '
                                                                       f'"{result["contour_set"]}" '
                                                                       f'{self.language["cells"].lower()}.')
        else:
            QMessageBox.about(self, self.language["error"], f'{self.language["error not found file"]}!')

    def open_dialog_params(self):
        """
        Функция для открытия окна для настройки параметров сканирования
        :return:
        """
        self.method.dialogParams.show()

    def choose_image(self):
        """
        Функция выбора картинки
        :return:
        """
        fname = QFileDialog.getOpenFileName(self, self.language['choose a picture'], "./",
                                            f'{self.language["picture"]} '
                                            f'({self.formatToScanComboBox.currentText()}))')[0]
        if fname:
            self.folderToScanLineEdit.setText("")
            self.fileToScanLineEdit.setText(fname)
        else:
            self.fileToScanLineEdit.setText("")

    def choose_folder_to_scan(self):
        """
        Функция выбора папки для сканирования
        :return:
        """
        folder_path = QFileDialog.getExistingDirectory(self, self.language["choose a folder"], "./")
        if folder_path:
            self.fileToScanLineEdit.setText("")
            self.folderToScanLineEdit.setText(folder_path)
        else:
            self.folderToScanLineEdit.setText("")

    def choose_folder_to_save(self):
        """
        Функция выбора папки для сохранения
        :return:
        """
        folder_path = QFileDialog.getExistingDirectory(self, self.language["choose a folder"], "./")
        if folder_path:
            self.scanToFolderLineEdit.setText(folder_path)
        else:
            self.scanToFolderLineEdit.setText("")

    def set_language(self, language):
        """
        Установка локализации текста
        :param language: Файл с локализацией
        :return:
        """
        self.nameMethodLabel.setText(self.language.get(self.method.NAME, self.method.NAME))

        for key, value in self.language.items():
            if key == "exit":
                self.exitButton.setText(value)

            if key == "cancel":
                self.cancelButton.setText(value)

            if key == "scanning":
                self.setWindowTitle(value)

            if key == "scan":
                self.scanButton.setText(value)

            if key == "file to scan":
                self.fileToScanLabel.setText(value + ":")

            if key == "folder to scan":
                self.folderToScanLabel.setText(value + ":")

            if key == "method":
                self.methodLabel.setText(value + ":")

            if key == "choose":
                self.chooseFileToScanPushButton.setText(value)
                self.chooseFolderToScanPushButton.setText(value)
                self.chooseScanToFolderPushButton.setText(value)

            if key == "setting method":
                self.settingsMethodsPushButton.setText(value)

            if key == "format to scan":
                self.formatToScanLabel.setText(value + ":")

            if key == "folder to scan":
                self.folderToScanLabel.setText(value + ":")

            if key == "file to scan":
                self.fileToScanLabel.setText(value + ":")

            if key == "folder to save":
                self.folderToSaveLabel.setText(value + ":")

            if key == "display final image":
                self.displayFinalImageCheckBox.setText(value)

    def cancel(self):
        """
        Функция для выхода в главное окно
        :return:
        """
        self.main_window.show()
        self.close()

    def exit_application(self):
        """
        Функция для закрытия окна
        :return:
        """
        self.close()
