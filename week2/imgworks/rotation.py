import cv2
import numpy as np

image = cv2.imread(r"C:\Users\chawa\Downloads\lenna.png")
cv2.imshow('Original image', image)
height, width = image.shape[:2]
M = cv2.getRotationMatrix2D((width / 2.0, height / 2.0), 180, 1)
dst_image = cv2.warpAffine(image, M, (width, height))
cv2.circle(dst_image, (round(width / 2.0), round(height / 2.0)), 5, (0, 255, 0), -1)
cv2.imshow('Image rotated 180 degrees',dst_image)
M_2 = cv2.getRotationMatrix2D((width / 1.5, height / 1.5), 30, 1)
dst_image_2 = cv2.warpAffine(image, M_2, (width, height))
cv2.circle(dst_image_2, (round(width / 1.5), round(height / 1.5)), 5, (0, 255, 0), -1)
cv2.imshow('Image rotated 30 degrees',dst_image_2)
cv2.waitKey(0)