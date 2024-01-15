import cv2
import numpy as np

image = cv2.imread('lenna_and_others.png')
cv2.imshow('Original image',image)
height, width = image.shape[:2]
image_points = image.copy()
cv2.circle(image_points, (135, 45), 5, (0, 0, 255), -1)
cv2.circle(image_points, (385, 45), 5, (0, 0, 255), -1)
cv2.circle(image_points, (135, 230), 5, (0, 0, 255), -1)
cv2.imshow('before affine transformation',image_points)
pts_1 = np.float32([[135, 45], [385, 45], [135, 230]])
pts_2 = np.float32([[135, 45], [385, 45], [150, 230]])
M = cv2.getAffineTransform(pts_1, pts_2)
dst_image = cv2.warpAffine(image_points, M, (width, height))
cv2.imshow('Affine transformation',dst_image)
cv2.waitKey(0)