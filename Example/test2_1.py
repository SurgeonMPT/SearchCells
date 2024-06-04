import cv2
import numpy as np
from matplotlib import pyplot as plt


def increase_intensity(img, center, strength):
    height, width = img.shape[:2]
    y, x = center  # Координаты центра освещенности

    # Создаем сетку координат, чтобы рассчитать расстояние от каждой точки до центра
    Y, X = np.ogrid[:height, :width]
    distances = np.sqrt((X - x) ** 2 + (Y - y) ** 2)

    # Нормализуем расстояния от 0 до 1
    max_distance = np.max(distances)
    distances /= max_distance

    # Увеличиваем интенсивность в зависимости от расстояния
    img = np.add(img, (1 - distances) * strength, out=img, casting="unsafe")

    # Ограничиваем значения интенсивности до 255
    img[img > 255] = 255

    return img.astype(np.uint8)


# Загрузка изображения
img = cv2.imread('5a-50lum-10x-365-2.tif', cv2.IMREAD_GRAYSCALE)

# Задаем центр освещенности и силу покрытия (можете изменить по вашему усмотрению)
center = (2700, 700)  # Примерные координаты центра освещенности
strength = 10  # Примерная сила покрытия

# Увеличение интенсивности
result_img = increase_intensity(img.copy(), center, strength)

# Вывод результата
plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
