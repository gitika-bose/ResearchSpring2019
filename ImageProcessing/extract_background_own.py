# Finds the mean of a template (say 25 * 25 pixels)
# and check which pixel in the image is within mean and std.

import numpy as np
import cv2
import imutils
import math
import sys

def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

img2 = cv2.imread(sys.argv[1])
img = img2.copy()
# img = imutils.resize(img, width=300)
# display("Original", img)
w, h = img.shape[:2]
# print(w, h)
wi, hi = 25, 25
template = img[:wi, :hi] # top left
template2 = img[w-wi:, h-hi:] # bottom right
template3 = img[w-wi:, :hi] # top right
template4 = img[:wi, h-hi:] # bottom left
# display("Template", template)

B, G, R = [], [], []
for i in range(wi):
    for j in range(hi):
        pixel = template[i][j]
        pixel2 = template2[i][j]
        pixel3 = template3[i][j]
        pixel4 = template4[i][j]
        # print(pixel)
        B.extend((pixel[0], pixel2[0], pixel3[0], pixel4[0]))
        G.extend((pixel[1], pixel2[1], pixel3[1], pixel4[1]))
        R.extend((pixel[2], pixel2[2], pixel3[2], pixel4[2]))

sB, sG, sR = math.ceil(np.std(B)), math.ceil(np.std(G)), math.ceil(np.std(R))
mB, mG, mR = int(np.mean(B)), int(np.mean(G)), int(np.mean(R))
# sB, sG, sR = np.std(B), np.std(G), np.std(R)
# mB, mG, mR = np.mean(B), np.mean(G), np.mean(R)
# print(mB, sB)
# print(mG, sG)
# print(mR, sR)
for i in range(w):
    for j in range(h):
        pixel = img[i][j]
        if abs(pixel[0]-mB) <= sB and abs(pixel[1]-mG) <= sG and abs(pixel[2]-mR) <= sR:
            img[i][j] = [0, 0, 0]

# display("New Image", img)
cv2.imwrite('extract_background_own_img.jpg', img)