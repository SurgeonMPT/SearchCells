import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from skimage import color, measure


# Класс алгоритма
class ScanningAlgorithmV3:
    NAME = 'Водораздел'

    # Функция иницилизации
    def __init__(self):
        self.dialogParams = DialogParamsMethod()

    # Функция для добавления конрастности и яркости картинки
    def adjust_contrast_brightness(self, img, contrast: float = 1.0, brightness: int = 0):
        """
        Adjusts contrast and brightness of an uint8 image.
        contrast:   (0.0,  inf) with 1.0 leaving the contrast as is
        brightness: [-255, 255] with 0 leaving the brightness as is
        """
        brightness += int(round(255 * (1 - contrast) / 2))
        return cv2.addWeighted(img, contrast, img, 0, brightness)

    # Функция для старта сканирования изображения
    def scan(self, data_params):
        print(f'Testing {ScanningAlgorithmV3.NAME} method')
        file = data_params['file_to_scan']
        size_pixel = data_params['dop_params']['size_pixel']
        k = data_params['dop_params']['k']

        img1 = cv2.imread(file)
        # Преобразование в шкалу черно-белого
        img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        # Попытка исправить ситуацию за счет контрастности картинки
        # img_hist = cv2.equalizeHist(img)
        img_hist = self.adjust_contrast_brightness(img, 0.8, brightness=-30)

        # Показ в сером стиле
        # cv2.imshow("Blue image", img)
        # cv2.imshow("Blue image1", img_hist)
        # cv2.waitKey(0)
        # ----
        img = img_hist

        pixel_to_um = size_pixel  # 1 пиксель = 454 nm

        # Фильтрация по порогам
        ret1, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        sure_bg = cv2.dilate(opening, kernel, iterations=2)
        # Показ контура
        # cv2.imshow("Sure Background", sure_bg)
        # cv2.waitKey(0)
        # ----

        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)
        ret2, sure_bg = cv2.threshold(dist_transform, k * dist_transform.max(), 255, 0)

        sure_fg = np.uint8(sure_bg)

        # Показ контура
        # cv2.imshow("Sure Faceground", sure_fg)
        # cv2.waitKey(0)
        # ----

        unknown = cv2.subtract(sure_bg, sure_fg, dtype=cv2.CV_8U)
        ret3, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 10
        markers[unknown==255] = 0

        markers = cv2.watershed(img1, markers)
        # Цвет BGR СИНИЙ ЗЕЛЕНЫЙ КРАСНЫЙ
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
            'method_name': ScanningAlgorithmV3.NAME,
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
