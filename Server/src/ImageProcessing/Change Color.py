
original_image_path

img = cv2.imread(original_image_path, 0)

img[mask == 255] = [0, 0, 255]
