# 'scan/ht-29/5a-50lum-10x-365-2.tif'

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загрузка изображения
image_path = 'scan/ht-29/5a-50lum-10x-365-2.tif'
image = cv2.imread(image_path, 0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Применение градиента Собеля для выделения границ
gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

# Применение порогового значения для выделения границ
ret, thresholded_image = cv2.threshold(gradient, 20, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Применение операции морфологического открытия для удаления шума и замыкания границ
opening = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, kernel)

# Применение дилатации для увеличения ширины границ
dilated = cv2.dilate(opening, kernel, iterations=2)

# Доработка 3: Применение операции закрытия
closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

# Доработка 4: Применение алгоритма watershed
dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 3)
ret, sure_fg = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(closing, sure_fg)
ret, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# Преобразование в трехканальное изображение
image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
# Применение алгоритма watershed
markers = cv2.watershed(image_bgr, markers)

# Наложение маски для выделения границ объектов
image_with_boundaries = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
image_with_boundaries[markers == -1] = [0, 0, 255]  # Цвет границ красный

# Отображение изображений
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title('Исходное изображение')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(image_with_boundaries)
plt.title('Обнаруженные границы')
plt.axis('off')

plt.show()