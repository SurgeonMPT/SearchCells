from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from classes.scan_window import ScanWindow
from classes.helpers import exist_file, exit_app, write_dict_file_txt
from scan_models.scanning_algorithm_v0 import ScanningAlgorithmV0
from scan_models.scanning_algorithm_v1 import ScanningAlgorithmV1
from scan_models.scanning_algorithm_v2 import ScanningAlgorithmV2
from scan_models.scanning_algorithm_v3 import ScanningAlgorithmV3
from scan_models.scanning_algorithm_v3_1 import ScanningAlgorithmV31
from scan_models.scanning_algorithm_v3_2 import ScanningAlgorithmV32


# Класс окна
class MainWindow(QMainWindow):
    # Инициализация свойств класса
    def __init__(self):
        super().__init__()
        self.scan_window = None
        self.initUI()

        self.exitButton.clicked.connect(exit_app)
        self.chooseButton.clicked.connect(self.choose_image)
        self.scanButton.clicked.connect(self.scan)

        # Установка стандартных настроек
        self.default_path = 'scan/ht-29/5a-50lum-10x-365-2.tif'
        self.pathTextEdit.setText(exist_file(self.default_path))

        self.algComboBox.addItems([ScanningAlgorithmV0.NAME, ScanningAlgorithmV1.NAME,
                                   ScanningAlgorithmV2.NAME, ScanningAlgorithmV3.NAME,
                                   ScanningAlgorithmV31.NAME, ScanningAlgorithmV32.NAME])
        self.algComboBox.setCurrentIndex(0)

    # Функция для отображения внешнего вида окна
    def initUI(self):
        uic.loadUi('./templates/main_window.ui', self)

    # Функция выбора файла
    def choose_image(self):
        path = exist_file(self.default_path)

        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', path, 'Картинка (*.tif)')[0]
        if fname:
            self.pathTextEdit.setText(fname)
        else:
            self.pathTextEdit.setText(path)

    # Функция сканирования
    def scan(self):
        if exist_file(self.pathTextEdit.toPlainText()) and self.algComboBox.currentIndex() >= 0:
            setting = {
                'scan_path': self.pathTextEdit.toPlainText(),
                'algorithm': str(self.algComboBox.currentIndex()),
                'k': str(self.kDoubleSpinBox.value()),
                'size_pixel': str(self.sizePixelDoubleSpinBox.value())
            }
            write_dict_file_txt('setting', setting)
            self.scan_window = ScanWindow(self)
            self.scan_window.show()
            self.hide()
        elif not exist_file(self.pathTextEdit.toPlainText()):
            QMessageBox.about(self, 'Ошибка', f'Выбранный файл не существует "{self.pathTextEdit.toPlainText()}"')
        elif self.algComboBox.currentIndex() < 0:
            QMessageBox.about(self, 'Ошибка', f'Не выбран алгоритм для сканирования')
