import cv2
import numpy as np

# Open the image. 
img = cv2.imread('5a-50lum-10x-365-2.tif')

# Trying 4 gamma values. 
for gamma in [0.1, 0.5]:
    # Apply gamma correction.
    gamma_corrected = np.array(255 * (img / 255) ** gamma, dtype='uint8')

    # Save edited images. 
    cv2.imwrite('gamma_transformed' + str(gamma) + '.tif', gamma_corrected)