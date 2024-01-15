import cv2
import numpy as np

image = cv2.imread(r"C:\Users\chawa\Downloads\lenna.png")
cv2.imshow('Original image',image)
height, width = image.shape[:2]
M = np.float32([[1, 0, 60], [0, 1, 15]])
dst_image = cv2.warpAffine(image, M, (width, height))
cv2.imshow('Translated image (positive values)',dst_image)
M_2 = np.float32([[1, 0, -60], [0, 1, -15]])
dst_image_2 = cv2.warpAffine(image, M_2, (width, height))
cv2.imshow('Translated image (negative values)', dst_image_2)
cv2.waitKey(0)