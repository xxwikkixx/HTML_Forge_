# filename = 'IMG_1536.JPG'

import cv2
import numpy as np

filename = 'IMG_1536.JPG'
img = cv2.imread(filename)
# img_bin = cv2.resize(img, (300, 200))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 1, 0.04)

# result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst > 0.5 * dst.max()] = [0, 0, 255]

cv2.imshow('dst', img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
