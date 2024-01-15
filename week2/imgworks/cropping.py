import cv2
import numpy as np

image = cv2.imread(r"C:\Users\chawa\Downloads\lenna.png")
cv2.imshow('Original image',image)
height, width = image.shape[:2]
image_points = image.copy()
cv2.circle(image_points, (230, 80), 5, (0, 0, 255),-1)
cv2.circle(image_points, (330, 80), 5, (0, 0, 255),-1)
cv2.circle(image_points, (230, 200), 5, (0, 0, 255),-1)
cv2.circle(image_points, (330, 200), 5, (0, 0, 255),-1)
cv2.line(image_points, (230, 80), (330, 80), (0, 0, 255))
cv2.line(image_points, (230, 200), (330, 200), (0, 0, 255))
cv2.line(image_points, (230, 80), (230, 200), (0, 0, 255))
cv2.line(image_points, (330, 200), (330, 80), (0, 0, 255))
cv2.imshow('Before cropping',image_points)

dst_image = image[80:200, 230:330]
cv2.imshow('Cropping image',dst_image)

cv2.waitKey(0)