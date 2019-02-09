import cv2
import numpy as np

img = cv2.imread('IMG_1536.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 255, 255, apertureSize=3)

# (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Threshold and contrast the image
# edges = cv2.resize(edges, (3000, 2000))


cv2.imwrite('cann.jpg', edges)
lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180, threshold=20, minLineLength=150, maxLineGap=30)

print(len(lines))

for i in range(0,len(lines)):
    x1, y1, x2, y2 = lines[i][0]
    print(x1, y1, x2, y2)
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 8)

cv2.imwrite('houghlines5.jpg', img)
cv2.destroyAllWindows()
