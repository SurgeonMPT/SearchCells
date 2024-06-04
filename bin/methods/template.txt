import os
import cv2
import matplotlib.pyplot as plt


class ScanningAlgorithmV5:
    """
    Класс алгоритма
    """
    NAME = 'Поиск локальный максимумов'

    def __init__(self):
        """
        Функция инициализации
        """
        self.dialogParams = None

    def scan(self, data_params):
        """
        Функция для старта сканирования изображения
        :param data_params: Параметры сканирования
        :return: Данные сканирования
        """
        file = data_params['file_to_scan']
        print(f'Testing {ScanningAlgorithmV5.NAME} method')
        img1 = cv2.imread(file)

        img2 = cv2.imread(file)
        cell_number = 0
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
            'method_name': ScanningAlgorithmV5.NAME,
            'contour_set': cell_number,
            'path_file': data_params['folder_to_save'] + f'\\result_cells_{cell_number}_' + os.path.basename(file)
        }
