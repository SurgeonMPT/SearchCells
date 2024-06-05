import os
import cv2
from glob import glob

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from skimage import io
import matplotlib.pyplot as plt
from skimage.filters import gaussian
from skimage.feature import peak_local_max


class ScanningAlgorithmV5:
    """
    Класс алгоритма
    """
    NAME = 'Поиск локальный максимумов'

    def __init__(self):
        """
        Функция инициализации
        """
        self.dialogParams = DialogParamsMethod()

    # Функция для определения центров клеток
    def detect_nuclei(self, img, sigma=5.5, min_distance=2, threshold_abs=110):
        g = gaussian(img, sigma, preserve_range=True)
        peaks = peak_local_max(g, min_distance, threshold_abs, exclude_border=False)
        return peaks

    def scan(self, data_params):
        """
        Функция для старта сканирования изображения
        :param data_params: Параметры сканирования
        :return: Данные сканирования
        """
        print(data_params)
        file = data_params['file_to_scan']
        print(f'Testing {ScanningAlgorithmV5.NAME} method')

        img1 = io.imread(file)

        gray_img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        print(img1.shape, img1.dtype, img1.min(), img1.max())

        # Находим центры
        print(data_params['dop_params'])
        centers = self.detect_nuclei(gray_img, data_params['dop_params']['sigma'],
                                     data_params['dop_params']['min distance'],
                                     data_params['dop_params']['threshold abs'])

        img2 = cv2.imread(file)
        cell_number = len(centers)
        if data_params['show_image']:
            plt.figure(f'{file}. {data_params["language"]["cells"]}: {cell_number}', figsize=(12, 6))
            plt.suptitle(f'{file}. {data_params["language"]["cells"]}: {cell_number}', fontsize=16)

            # Отображение первого изображения
            plt.subplot(1, 2, 1)
            plt.imshow(img1, cmap='gray')
            plt.title(f'{data_params["language"]["cells"]}: {cell_number} - img1')
            plt.axis('off')

            # Отображение второго изображения
            plt.subplot(1, 2, 2)
            plt.imshow(img1, cmap='gray', vmax=4000)
            plt.plot(centers[:, 1], centers[:, 0], 'r.')
            plt.title(f'{data_params["language"]["cells"]}: {cell_number} - img2')
            plt.axis('off')

            plt.tight_layout()
            plt.show()

        if data_params['folder_to_save']:
            save_path = os.path.join(data_params['folder_to_save'],
                                     f'result_cells_{cell_number}_{os.path.basename(file)}')
            plt.savefig(save_path)

        return {
            'method_name': ScanningAlgorithmV5.NAME,
            'contour_set': cell_number,
            'path_file': data_params['folder_to_save'] + f'\\result_cells_{cell_number}_' + os.path.basename(file)
        }


class DialogParamsMethod(QDialog):
    """
    Класс диалогового окна с параметрами системы
    """
    def __init__(self):
        """
        Инициализация свойств
        """
        super().__init__()
        self.params = {
            'sigma': 5.5,
            'min distance': 2,
            'threshold abs': 110
        }
        self.is_accept = False
        self.initUI()

    def initUI(self):
        """
        Функция для отображения внешнего вида окна
        :return: Нет
        """
        uic.loadUi('./resources/templates/dialog_scanning_algorithm_v5.ui', self)
        self.setWindowIcon(QIcon('./resources/images/icon.ico'))
        self.sigmaDoubleSpinBox.setValue(self.params["sigma"])
        self.minDistanceDoubleSpinBox.setValue(self.params["min distance"])
        self.thresholdAbsDoubleSpinBox.setValue(self.params["threshold abs"])
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def set_language(self, language):
        """
        Функция для установки локализации
        :param language: Язык
        :return:
        """
        for key, value in language.items():
            if key == "cancel":
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(value)

            if key == "ok":
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(value)

            if key == "method parameters":
                self.setWindowTitle(value)

            if key == "parameter sigma":
                self.paramSigmaLabel.setText(value + ":")

            if key == "min distance":
                self.minDistanceLabel.setText(value + ":")

            if key == "threshold abs":
                self.thresholdAbsLabel.setText(value + ":")

    def accept(self):
        """
        Обработчик нажатия кнопки "OK"
        """
        self.params = {
            'sigma': self.sigmaDoubleSpinBox.value(),
            'min distance': self.minDistanceDoubleSpinBox.value(),
            'threshold abs': self.thresholdAbsDoubleSpinBox.value(),
        }
        super().accept()
