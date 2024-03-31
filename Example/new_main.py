import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def print_hist(image_, label=""):
    plt.figure(label)
    plt.xlabel('bins')
    plt.ylabel('# of pixels')
    hist = cv2.calcHist([image_], [0], None, [256], [2, 256])
    plt.plot(hist, drawstyle='steps-mid')
    plt.xlim([0, 256])
    plt.ylim([0, hist.max() + 1])


def print_image(image_, label=""):
    plt.figure(label)
    plt.axis("off")
    plt.imshow(image_)


def print_contours(image_rgb, contours_set, label=""):
    color = [255, 255, 255]
    stencil = np.zeros(image_rgb.shape).astype(image_rgb.dtype)
    cv2.fillPoly(stencil, contours_set, color)
    selected_print = cv2.bitwise_and(image_rgb.copy(), stencil)
    cv2.drawContours(selected_print, contours_set, -1, (255, 0, 0), 2)
    print_image(selected_print)


def gaussian(sigma, mu, bins, maximum=1):
    # c = (sigma * np.sqrt(2 * np.pi))
    val = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (bins - mu) ** 2 / (2 * sigma ** 2))
    val = maximum * val / np.max(val)
    return val


def remove_background(image):
    height, width = image.shape
    pixel_num = np.arange(0, width, 1)
    for row in range(0, height):
        pfit = np.polyfit(pixel_num, image[row], 3)
        background = np.polyval(pfit, pixel_num)  # .astype(np.uint8)
        new_line = (image[row] - background)
        filtered_array = np.where(new_line > 0, new_line, 0).astype(np.uint8)
        # plt.figure()
        # plt.xlabel('pixel')
        # plt.ylabel(f'{row}')
        # plt.plot(pixel_num, line, 'b',
        #          pixel_num, background, 'r',
        #          pixel_num, filtered_array, 'g')
        image[row] = filtered_array
    return image


def amplify(image):
    max_val = image.max()
    image_ = int(255 * (float(image) / max_val))
    return image_


def line_is_not_belongs_to_border(line, width, height):
    width = (width - 1)
    height = (height - 1)
    for point in line:
        if (point[0][0] == 0) or (point[0][1] == 0) or (point[0][0] == width) or (point[0][1] == height):
            return False
    return True


def contour_is_bigger_than(min_width: int, min_height: int, contour_):
    y = contour_[:, 0, 0]
    x = contour_[:, 0, 1]
    (top_y, top_x) = (np.min(y), np.min(x))
    (bottom_y, bottom_x) = (np.max(y), np.max(x))
    width = bottom_x - top_x
    height = bottom_y - top_y

    return (width >= min_width) & (height >= min_height)


def save_contour(image_grayscale, contour_set, contour_num):
    stencil = np.zeros(image_grayscale.shape).astype(image_grayscale.dtype)
    cv2.fillPoly(stencil, contour_set[contour_num:contour_num + 1], 255)

    mask = np.zeros_like(image_grayscale)  # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, contour_set, contour_num, 255, -1)  # Draw filled contour in mask
    out = np.zeros_like(image_grayscale)  # Extract out the object and place into output image
    out[mask == 255] = image_grayscale[mask == 255]

    (y, x) = np.where(mask == 255)
    (top_y, top_x) = (np.min(y), np.min(x))
    (bottom_y, bottom_x) = (np.max(y), np.max(x))

    out = out[top_y:bottom_y + 1, top_x:bottom_x + 1]
    # print_image(out, f'cropped contour # {contour_num}')
    cv2.imwrite(f'Results\cell_{contour_num}.tif', out)


def cell_counting(file_, threshold_low, threshold_top=255, minimum_length=1, blur=1, color="gray"):
    image = cv2.imread(file_)  # ,cv2.IMREAD_GRAYSCALE)
    channels = cv2.split(image)
    if color == "red":
        image_channel = channels[2]
    elif color == "green":
        image_channel = channels[1]
    elif color == "blue":
        image_channel = channels[0]
    else:
        image_channel = cv2.imread(file_)  # ,cv2.IMREAD_GRAYSCALE)
        # cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # image #

    image_channel = cv2.fastNlMeansDenoising(image_channel, None, 20, 7, 21)
    # blur = 5
    image_channel = cv2.GaussianBlur(image_channel, (2 * blur + 1, 2 * blur + 1), 0)
    ret, image_channel = cv2.threshold(image_channel, threshold_low, 255, cv2.THRESH_BINARY)

    # plt.figure()
    # plt.axis("off")
    # plt.title('Gray')
    # plt.imshow(gray, cmap='gray')

    canny = cv2.Canny(image_channel, threshold_low, threshold_top, 4)
    canny = cv2.dilate(canny, (1, 1), iterations=0)
    (cnt, hierarchy) = cv2.findContours(
        canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # minimum_lenght = 200
    new_cnt = tuple(
        item for item in cnt if item.size > minimum_length
    )
    height, width = canny.shape
    new_cnt = tuple(
        line for line in new_cnt if (line_is_not_belongs_to_border(line, width=width, height=height))
    )

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure("basic")
    plt.axis("off")
    cv2.drawContours(rgb, new_cnt, -1, (255, 0, 0), 2)
    plt.imshow(rgb)  # , cmap='gray')
    #
    print(f'{file} basic, cells in the image : {len(new_cnt)}')
    # plt.show()
    return len(new_cnt)


def cell_counting_image(image_, noise_treshold=5, threshold_low=10, threshold_top=255, minimum_length=1, blur=1,
                        color="gray", exlude_corner=True):
    image_channel = image_
    # = cv2.fastNlMeansDenoising(image_channel, None, 20, 7, 21)
    # blur = 5
    image_channel = cv2.GaussianBlur(image_channel, (2 * blur + 1, 2 * blur + 1), 0)
    ret, image_channel = cv2.threshold(image_channel, noise_treshold, 255, cv2.THRESH_BINARY)

    canny = cv2.Canny(image_channel, threshold_low, threshold_top, 1)

    # kernel = np.ones((1, 1), np.uint8)
    # canny = cv2.erode(canny, kernel, iterations=1)

    canny = cv2.dilate(canny, (1, 1), iterations=0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(canny.copy(), cv2.MORPH_CLOSE, kernel)

    (cnt, hierarchy) = cv2.findContours(
        closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    new_cnt = tuple(
        item for item in cnt if item.size > minimum_length
    )
    if exlude_corner:
        height, width = canny.shape
        new_cnt = tuple(
            line for line in new_cnt if (line_is_not_belongs_to_border(line, width=width, height=height))
        )
    return new_cnt


def optimal(file):
    image_grayscale = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    height, width = image_grayscale.shape
    # print_hist(image_grayscale, label="Grayscale hist")
    image_cleared = remove_background(image_grayscale)

    # print_hist(image_cleared, label="remove_background")
    #
    # bins = np.arange(0, 256, dtype=int)
    # gauss = gaussian(14, 37, bins, 16400)
    # plt.plot(bins, gauss)

    ret, mask = cv2.threshold(image_cleared, 15, 255, cv2.THRESH_BINARY)
    # apply mask to input image
    masked_image = cv2.bitwise_and(image_cleared, mask)

    # blur = 1
    # new_image = cv2.GaussianBlur(new_image, (2 * blur + 1, 2 * blur + 1), 2)

    # kernel = np.ones((1, 1), np.uint8)
    # canny = cv2.erode(canny, kernel, iterations=1)

    canny = cv2.Canny(masked_image, 50, 65, 0)
    dilated = cv2.dilate(canny, (2, 2), iterations=3)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(dilated.copy(), cv2.MORPH_CLOSE, kernel)

    contour, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_filtered_by_length = tuple(item for item in contour if item.size > 50)
    contour_filtered_by_size = tuple(item for item in contour_filtered_by_length if contour_is_bigger_than(4, 4, item))
    # contour_filtered_by_border = tuple(line for line in contour_filtered_by_length if (line_is_not_belongs_to_border(line, width=width, height=height)))
    contour_set = contour_filtered_by_size
    image_cleared_rgb = cv2.cvtColor(image_cleared, cv2.COLOR_GRAY2RGB)
    stencil = np.zeros(image_cleared_rgb.shape).astype(image_cleared_rgb.dtype)
    color = [255, 255, 255]
    for cnt in contour_set:
        cv2.fillPoly(stencil, contour_set, color)
    result = cv2.bitwise_and(image_cleared_rgb.copy(), stencil)

    result_contoured = cv2.drawContours(result.copy(), contour_set, -1, (255, 0, 0), 2)
    print_image(result_contoured, "full")
    print(f'{file} cells in the image : {len(contour_set)}')
    return contour_set


def filter_by_threshold(threshold_value, canny_low, canny_top, image_cleared):
    height, width = image_cleared.shape
    ret, mask = cv2.threshold(image_cleared, threshold_value, 255, cv2.THRESH_BINARY)
    masked_image = cv2.bitwise_and(image_cleared, mask)

    canny = cv2.Canny(masked_image, canny_low, canny_top, 0)
    dilated = cv2.dilate(canny, (2, 2), iterations=7)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(dilated.copy(), cv2.MORPH_CLOSE, kernel)

    contour, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_filtered_by_length = tuple(item for item in contour if item.size > 50)
    # contour_filtered_by_border = tuple(line for line in contour_filtered_by_length if (line_is_not_belongs_to_border(line, width=width, height=height)))

    stencil = np.zeros(image_cleared.shape).astype(image_cleared.dtype)
    color = 255
    for cnt in contour_filtered_by_length:
        cv2.fillPoly(stencil, contour_filtered_by_length, color)
    cleaned_image = cv2.bitwise_not(image_cleared.copy(), stencil)
    return cleaned_image, contour_filtered_by_length


def adaptive_thresholding(file, blurr=11):
    image_grayscale = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    image_cleared_rgb = cv2.cvtColor(image_grayscale, cv2.COLOR_GRAY2RGB)

    mask = cv2.adaptiveThreshold(image_grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blurr, 2)
    masked_image = cv2.bitwise_and(image_grayscale, mask)

    canny = cv2.Canny(masked_image, 40, 65, 0)
    dilated = cv2.dilate(canny, (2, 2), iterations=3)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closed = cv2.morphologyEx(dilated.copy(), cv2.MORPH_CLOSE, kernel)

    contour, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_filtered_by_length = tuple(item for item in contour if item.size > 50)
    contour_filtered_by_size = tuple(item for item in contour_filtered_by_length if contour_is_bigger_than(4, 4, item))
    # contour_filtered_by_border = tuple(line for line in contour_filtered_by_length if (line_is_not_belongs_to_border(line, width=width, height=height)))
    contour_set = contour_filtered_by_size

    stencil = np.zeros(image_cleared_rgb.shape).astype(image_cleared_rgb.dtype)
    color = [255, 255, 255]
    for cnt in contour_set:
        cv2.fillPoly(stencil, contour_set, color)
    result = cv2.bitwise_and(image_cleared_rgb.copy(), stencil)

    result_contoured = cv2.drawContours(result.copy(), contour_set, -1, (255, 0, 0), 2)
    print_image(result_contoured, "full")
    print(f'{file} cells in the image : {len(contour_set)}')
    return contour_set


def select_contour(contour_num: int, image_rgb, contours_set, print_result=False):
    #
    color = [255, 255, 255]

    stencil = np.zeros(image_rgb.shape).astype(image_rgb.dtype)
    cv2.fillPoly(stencil, contours_set[contour_num:contour_num + 1], color)
    selected_ = cv2.bitwise_and(image_rgb.copy(), stencil)

    if print_result:
        selected_print = cv2.drawContours(selected_.copy(), contours_set[contour_num:contour_num + 1], -1, (255, 0, 0),
                                          2)
        print_image(selected_print, f'contour #{contour_num}')

    return selected_


if __name__ == '__main__':
    file = 'scan/ht-29/5a-50lum-10x-365-2.tif'

    image_grayscale = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    image_rgb = cv2.cvtColor(image_grayscale, cv2.COLOR_GRAY2RGB)
    print_image(image_grayscale)

    methods = ['Fourier', 'NonFlatBackground', ]
    method = methods[1]

    if method == methods[0]:
        print(f'Testing {method} method')
        f = np.fft.fft2(image_grayscale)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))
        # magnitude_spectrum = 20 * np.log(np.abs(f))
        plt.figure()
        plt.subplot(121), plt.imshow(image_grayscale, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
        plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])

        wave_len = 1000
        rows, cols = image_grayscale.shape
        crow, ccol = rows // 2, cols // 2

        fshift[0:wave_len, :] = 0
        fshift[:, 0:wave_len] = 0
        fshift[rows - wave_len:rows, :] = 0
        fshift[:, cols - wave_len:cols] = 0

        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f)
        img_back = np.real(img_back)

        img_ffiltered = cv2.normalize(src=img_back, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,
                                      dtype=cv2.CV_8U)

        plt.figure()
        plt.subplot(121), plt.imshow(image_grayscale, cmap='gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img_ffiltered, cmap='gray')
        plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])

        plt.figure()
        plt.xlabel('bins')
        plt.ylabel('# of pixels')
        hist_orig = cv2.calcHist([image_grayscale], [0], None, [256], [3, 256])
        plt.subplot(121), plt.plot(hist_orig, drawstyle='steps-mid')
        plt.xlim([0, 256])
        plt.ylim([0, hist_orig.max() + 1])
        hist_ffiltered = cv2.calcHist([img_ffiltered], [0], None, [256], [3, 256])
        plt.subplot(122), plt.plot(hist_ffiltered, drawstyle='steps-mid')
        plt.xlim([0, 256])
        plt.ylim([0, hist_ffiltered.max() + 1])

        ret, mask = cv2.threshold(img_ffiltered, 10, 255, cv2.THRESH_BINARY)

        masked_image = cv2.bitwise_and(img_ffiltered, mask)
        canny = cv2.Canny(masked_image, 10, 255, 0)
        dilated = cv2.dilate(canny, (2, 2), iterations=3)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closed = cv2.morphologyEx(dilated.copy(), cv2.MORPH_CLOSE, kernel)

        contour, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_filtered_by_length = tuple(item for item in contour if item.size > 50)
        contour_filtered_by_size = tuple(
            item for item in contour_filtered_by_length if contour_is_bigger_than(4, 4, item))

        contour_set = contour_filtered_by_size
        image_cleared_rgb = cv2.cvtColor(img_ffiltered, cv2.COLOR_GRAY2RGB)
        stencil = np.zeros(image_cleared_rgb.shape).astype(image_cleared_rgb.dtype)
        color = [255, 255, 255]
        for cnt in contour_set:
            cv2.fillPoly(stencil, contour_set, color)
        result = cv2.bitwise_and(image_cleared_rgb.copy(), stencil)

        result_contoured = cv2.drawContours(result.copy(), contour_set, -1, (255, 0, 0), 2)
        print_image(result_contoured, "full")
        print(f'{file} cells in the image : {len(contour_set)}')

    elif method == methods[1]:
        print(f'Testing {method} method')

        height, width = image_grayscale.shape

        image_cleared = remove_background(image_grayscale)  # удаление фона по полиному 3 порядка

        ret, mask = cv2.threshold(image_cleared, 15, 255, cv2.THRESH_BINARY)

        masked_image = cv2.bitwise_and(image_cleared, mask)

        canny = cv2.Canny(masked_image, 50, 65, 0)
        dilated = cv2.dilate(canny, (2, 2), iterations=3)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closed = cv2.morphologyEx(dilated.copy(), cv2.MORPH_CLOSE, kernel)

        contour, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_filtered_by_length = tuple(item for item in contour if item.size > 50)  # фильтрация по длине
        contour_filtered_by_size = tuple(
            item for item in contour_filtered_by_length if contour_is_bigger_than(4, 4, item))  # по размеру объекта
        contour_filtered_by_border = tuple(line for line in contour_filtered_by_length if (
            line_is_not_belongs_to_border(line, width=width, height=height)))  # по касанию к границе
        contour_set = contour_filtered_by_size

        image_cleared_rgb = cv2.cvtColor(image_cleared, cv2.COLOR_GRAY2RGB)
        stencil = np.zeros(image_cleared_rgb.shape).astype(image_cleared_rgb.dtype)
        color = [255, 255, 255]
        for cnt in contour_set:
            cv2.fillPoly(stencil, contour_set, color)
        result = cv2.bitwise_and(image_cleared_rgb.copy(), stencil)

        result_contoured = cv2.drawContours(result.copy(), contour_set, -1, (255, 0, 0), 2)
        print_image(result_contoured, "full")
        print(f'{file} cells in the image : {len(contour_set)}')

    print('done')
    plt.show()