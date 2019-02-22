import numpy as np
import cv2
from matplotlib import pyplot as plt
import imutils

img = cv2.imread('pill_images/pill_10.jpg')
resized = imutils.resize(img, width=350)
img = resized
# blurred = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Thresholds
thresh_adaptive_mean = cv2.adaptiveThreshold(gray ,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
thresh_adaptive_gaussian = cv2.adaptiveThreshold(gray ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
thresh_binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
thresh_binary_inv = cv2.threshold(gray,120,255,cv2.THRESH_BINARY_INV)[1]
thresh_trunc = cv2.threshold(gray,120,255,cv2.THRESH_TRUNC)[1]
thresh_tozero = cv2.threshold(gray,120,255,cv2.THRESH_TOZERO)[1]
thresh_tozero_inv = cv2.threshold(gray,120,255,cv2.THRESH_TOZERO_INV)[1]
thresh_otsu_bin_inv = cv2.threshold(gray,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)[1]
thresh_otsu = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)[1]

cv2.imshow('Image',img)
cv2.imshow('Gray',gray)
cv2.imshow('Adaptive Mean',thresh_adaptive_mean)
cv2.imshow('Adaptive Gaussian',thresh_adaptive_gaussian)
cv2.imshow('Binary',thresh_binary)
cv2.imshow('Binary Inverse',thresh_binary_inv)
cv2.imshow('Trunc',thresh_trunc)
cv2.imshow('Torzero',thresh_tozero)
cv2.imshow('Torzero Inverse',thresh_tozero_inv)
cv2.imshow('Otsu',thresh_otsu)
cv2.imshow('Otsu Binary Inverse',thresh_otsu_bin_inv)

cv2.waitKey(0)