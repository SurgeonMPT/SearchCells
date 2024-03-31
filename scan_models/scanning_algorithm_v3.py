import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import color, measure
from skimage.segmentation import clear_border


# Класс алгоритма
class ScanningAlgorithmV3:
    NAME = 'Водораздел'

    # Функция иницилизации
    def __init__(self, data):
        self.file = ''
        self.k = data['k']
        self.size_pixel = data['size_pixel']

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
    def scan(self, file):
        self.file = file
        print(f'Testing {ScanningAlgorithmV3.NAME} method')

        img1 = cv2.imread(self.file)
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

        pixel_to_um = self.size_pixel  # 1 пиксель = 454 nm

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
        ret2, sure_bg = cv2.threshold(dist_transform, self.k * dist_transform.max(), 255, 0)

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

        # cv2.imshow('Overlay on original image', img1)
        # cv2.imshow('Color Cells', img2)
        # cv2.waitKey(0)

        regions = measure.regionprops(markers, intensity_image=img1)
        propList = ['Area', 'equivalent_diameter', 'orientation', 'MajorAxisLength',
                    'MinorAxisLength', 'Perimeter', 'MinIntensity', 'MeanIntensity', 'MaxIntensity']

        output_file = open('image_measurements.csv', 'w')
        output_file.write('Cell #' + "," + "," + ",".join(propList) + '\n')

        cell_number = 1
        for regions_props in regions:
            output_file.write(str(cell_number) + ',')

            for i, prop in enumerate(propList):
                if prop == 'Area':
                    to_print = regions_props[prop] * pixel_to_um ** 2
                elif prop == 'orientation':
                    to_print = regions_props[prop] * 57.2958
                elif prop.find('Intensity') < 0:
                    to_print = regions_props[prop] * pixel_to_um
                output_file.write(',' + str(to_print))
            output_file.write('\n')
            cell_number += 1

        output_file.close()

        cv2.imwrite('result.png', 255 * img2)

        return {
            'method_name': ScanningAlgorithmV3.NAME,
            'contour_set': cell_number,
            'path_file': 'result.png'
        }
