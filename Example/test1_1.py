import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загрузка изображения
image = cv2.imread('5a-50lum-10x-365-2.tif')

# Преобразование изображения в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применение пороговой обработки для выделения клеток
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Поиск контуров клеток
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Выделение контуров красным цветом и вычисление площади
average_area = 0
total_cells = 0
for contour in contours:
    # Вычисление ограничивающего прямоугольника для контура
    x, y, w, h = cv2.boundingRect(contour)
    center_x = x + w // 2
    center_y = y + h // 2
    if w > 10 and h > 10 and center_x > 10 and center_y > 10 and center_x < image.shape[1] - 10 and center_y < image.shape[0] - 10:
        # Игнорирование контуров, которые находятся на границе изображения
        area = cv2.contourArea(contour)
        if area > 0:
            average_area += area
            total_cells += 1
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)

# Вычисление средней площади клетки
average_area /= total_cells

# Удаление клеток с площадью менее 15% от среднего размера клеток
for contour in contours:
    area = cv2.contourArea(contour)
    if area < 0.15 * average_area:
        cv2.drawContours(image, [contour], -1, (255, 255, 255), -1)

# Вывод результата
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
