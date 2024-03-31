import cv2
import numpy as np
from skimage import color, measure


# Класс алгоритма
class ScanningAlgorithmV31:
    NAME = 'Водораздел с контурами'

    # Функция иницилизации
    def __init__(self, data):
        self.file = ''
        self.k = data['k']
        self.size_pixel = data['size_pixel']

    def get_contours(self, img):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    # Функция для старта сканирования изображения
    def scan(self, file):
        self.file = file
        print(f'Testing {ScanningAlgorithmV31.NAME} method')

        img1 = cv2.imread(self.file)
        img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        pixel_to_um = self.size_pixel

        ret1, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # Применение операции размыкания для разделения перекрывающихся клеток
        ret1, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        contours = self.get_contours(opening)

        if len(contours) > 0:
            cv2.drawContours(img1, contours, -1, (0, 0, 255), 2)
            markers = np.zeros_like(img, dtype=np.int32)
            for i, contour in enumerate(contours):
                cv2.drawContours(markers, [contour], 0, i + 1, -1)

            markers = cv2.watershed(img1, markers)
            img1[markers == -1] = [255, 255, 0]
            img2 = color.label2rgb(markers, bg_label=0)

            regions = measure.regionprops(markers, intensity_image=img1)
            propList = ['Area', 'equivalent_diameter', 'orientation', 'MajorAxisLength',
                        'MinorAxisLength', 'Perimeter', 'MinIntensity', 'MeanIntensity', 'MaxIntensity']

            output_file = open('image_measurements.csv', 'w')
            output_file.write('Cell #' + "," + "," + ",".join(propList) + '\n')

            cell_number = 1
            for regions_props in regions:
                output_file.write(str(cell_number) + ',')

                for i, prop in enumerate(propList):
                    to_print = ''
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
                'method_name': ScanningAlgorithmV31.NAME,
                'contour_set': cell_number,
                'path_file': 'result.png'
            }
        else:
            print('No contours found.')
            return None