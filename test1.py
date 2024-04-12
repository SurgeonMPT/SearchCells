# https://python-school.ru/blog/python/find-nuclei-with-skimage/
from glob import glob
import cv2
from skimage import io
import matplotlib.pyplot as plt
from skimage.filters import gaussian
from skimage.feature import peak_local_max


# Функция для определения центров клеток
def detect_nuclei(img, sigma=5.5, min_distance=2, threshold_abs=160):
    g = gaussian(img, sigma, preserve_range=True)
    peaks = peak_local_max(g, min_distance, threshold_abs, exclude_border=False)
    return peaks


# Главная функция
def main():
    # Загружаем изображения
    paths = glob('5a-50lum-10x-365-2.tif')
    paths.sort()
    if not paths:
        return

    # Обрабатываем изображения
    for path in paths:
        img = io.imread(path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(img.shape, img.dtype, img.min(), img.max())

        # Находим центры
        centers = detect_nuclei(gray_img)
        print(len(centers))

        # Отрисовка центром на изображении
        plt.figure(figsize=(6, 6))
        plt.imshow(img, cmap='gray', vmax=4000)
        plt.plot(centers[:, 1], centers[:, 0], 'r.')
        plt.axis('off')
        plt.savefig('result.tif')
        plt.show()


if __name__ == "__main__":
    main()
