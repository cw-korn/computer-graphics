import cv2
import numpy as np

image = cv2.imread(r"C:\Users\chawa\Downloads\lenna.png")
cv2.imshow('Original image',image)
dst_image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
height, width = image.shape[:2]
dst_image_2 = cv2.resize(image, (width * 2, height * 2),interpolation=cv2.INTER_AREA)
cv2.imshow('Resized image (50%)',dst_image)
cv2.imshow('Resized image (200%)',dst_image_2)
cv2.waitKey(0)
