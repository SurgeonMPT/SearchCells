from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from classes.helpers import exit_app, read_dict_file_txt, remove_file
from scan_models.scanning_algorithm_v0 import ScanningAlgorithmV0
from scan_models.scanning_algorithm_v1 import ScanningAlgorithmV1
from scan_models.scanning_algorithm_v2 import ScanningAlgorithmV2
from scan_models.scanning_algorithm_v3 import ScanningAlgorithmV3
from scan_models.scanning_algorithm_v3_1 import ScanningAlgorithmV31
from scan_models.scanning_algorithm_v3_2 import ScanningAlgorithmV32


# Класс окна
class ScanWindow(QMainWindow):
    # Инициализация свойств класса
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

        self.backButton.clicked.connect(self.back_window)
        self.exitButton.clicked.connect(exit_app)
        self.showOrigButton.clicked.connect(self.show_orig)
        self.showScanButton.clicked.connect(self.scan)

        # Загружаем настройки
        self.setting = read_dict_file_txt('setting')
        remove_file('setting.txt')
        self.alg = None

        if int(self.setting['algorithm']) == 0:
            self.alg = ScanningAlgorithmV0()
        elif int(self.setting['algorithm']) == 1:
            self.alg = ScanningAlgorithmV1()
        elif int(self.setting['algorithm']) == 2:
            self.alg = ScanningAlgorithmV2()
        elif int(self.setting['algorithm']) == 3:
            data = {
                'k': float(self.setting['k']),
                'size_pixel': float(self.setting['size_pixel'])
            }
            self.alg = ScanningAlgorithmV3(data)
        elif int(self.setting['algorithm']) == 4:
            data = {
                'k': float(self.setting['k']),
                'size_pixel': float(self.setting['size_pixel'])
            }
            self.alg = ScanningAlgorithmV31(data)
        elif int(self.setting['algorithm']) == 5:
            data = {
                'k': float(self.setting['k']),
                'size_pixel': float(self.setting['size_pixel'])
            }
            self.alg = ScanningAlgorithmV32(data)

        self.show_orig()

    # Функция для отображения внешнего вида окна
    def initUI(self):
        uic.loadUi('./templates/scan_window.ui', self)

    # Функция возврата в предыдущее приложение
    def back_window(self):
        self.main_window.show()
        self.hide()

    # Функция отображения оригинала
    def show_orig(self):
        pixmap = QPixmap(self.setting['scan_path'])
        self.scanLabel.setPixmap(pixmap)

    # Функция сканирования
    def scan(self):
        result = self.alg.scan(self.setting['scan_path'])
        if result:
            self.statusLabel.setText(f'{result["method_name"]}: {result["contour_set"]}')
            pixmap = QPixmap(result['path_file'])
            self.scanLabel.setPixmap(pixmap)
