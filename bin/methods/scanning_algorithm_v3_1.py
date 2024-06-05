import os

import cv2
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from matplotlib import pyplot as plt
from skimage import color, measure


# Класс алгоритма
class ScanningAlgorithmV31:
    NAME = 'Водораздел с контурами'

    # Функция иницилизации
    def __init__(self):
        self.dialogParams = DialogParamsMethod()

    def get_contours(self, img):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    # Функция для старта сканирования изображения
    def scan(self, data_params):
        file = data_params['file_to_scan']
        size_pixel = data_params['dop_params']['size_pixel']
        k = data_params['dop_params']['k']

        print(f'Testing {ScanningAlgorithmV31.NAME} method')

        img1 = cv2.imread(file)
        img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        pixel_to_um = size_pixel

        ret1, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # Применение операции размыкания для разделения перекрывающихся клеток
        ret1, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        contours = self.get_contours(opening)

        cv2.drawContours(img1, contours, -1, (0, 0, 255), 2)
        markers = np.zeros_like(img, dtype=np.int32)
        for i, contour in enumerate(contours):
            cv2.drawContours(markers, [contour], 0, i + 1, -1)

        markers = cv2.watershed(img1, markers)
        img1[markers == -1] = [255, 255, 0]
        img2 = color.label2rgb(markers, bg_label=0)

        regions = measure.regionprops(markers, intensity_image=img1)
        cell_number = len(regions)

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
            plt.imshow(img2, cmap='gray')
            plt.title(f'{data_params["language"]["cells"]}: {cell_number} - img2')
            plt.axis('off')

            plt.tight_layout()
            plt.show()

        if data_params['folder_to_save']:
            save_path = os.path.join(data_params['folder_to_save'],
                                     f'result_cells_{cell_number}_{os.path.basename(file)}')
            plt.savefig(save_path)

        return {
            'method_name': ScanningAlgorithmV31.NAME,
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
            'k': 0.5,
            'size_pixel': 0.454
        }
        self.is_accept = False
        self.initUI()

    def initUI(self):
        """
        Функция для отображения внешнего вида окна
        :return: Нет
        """
        uic.loadUi('./resources/templates/dialog_scanning_algorithm_v3.ui', self)
        self.setWindowIcon(QIcon('./resources/images/icon.ico'))
        self.kDoubleSpinBox.setValue(self.params["k"])
        self.sizePixelDoubleSpinBox.setValue(self.params["size_pixel"])
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

            if key == "parameter k":
                self.paramKLabel.setText(value + ":")

            if key == "size pixel":
                self.sizePixelLabel.setText(value + ":")

    def accept(self):
        """
        Обработчик нажатия кнопки "OK"
        """
        self.params = {
            'k': self.kDoubleSpinBox.value(),
            'size_pixel': self.sizePixelDoubleSpinBox.value(),
        }
        super().accept()
