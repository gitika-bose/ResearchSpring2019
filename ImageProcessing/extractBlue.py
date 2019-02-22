import cv2
import numpy as np
import sys

image = cv2.imread(sys.argv[1])

# # Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#
# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(image,image, mask= mask)
#
cv2.imshow('image',image)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
cv2.waitKey(0)
