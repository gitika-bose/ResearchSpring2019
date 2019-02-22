# records different colors within the template (say 25 * 25 pixels)
# and check which pixel in the image is within the list of colors

import numpy as np
import cv2
import imutils
import math

img2 = cv2.imread('pill_images/pill_10_bottom.jpg')
img = img2.copy()
# img = imutils.resize(img, width=300)
cv2.imshow("Original", img)
cv2.waitKey(0)
w, h = img.shape[:2]
print(w, h)
wi, hi = 25, 25
template = img[:wi, :hi] # top left
template2 = img[w-wi:, h-hi:] # bottom right
template3 = img[w-wi:, :hi] # top right
template4 = img[:wi, h-hi:] # bottom left
# cv2.imshow("Template", template)
B, G, R = [300,0], [300,0], [300,0]
# bgr = set()
for i in range(wi):
    for j in range(hi):
        pixel = template[i][j]
        pixel2 = template2[i][j]
        pixel3 = template3[i][j]
        pixel4 = template4[i][j]
        B[0], B[1] = min(int(pixel[0]), int(pixel2[0]), int(pixel3[0]), int(pixel4[0]), B[0]), \
                     max(math.ceil(pixel[0]), math.ceil(pixel2[0]), math.ceil(pixel3[0]), math.ceil(pixel4[0]), B[1])
        G[0], G[1] = min(int(pixel[1]), int(pixel2[1]), int(pixel3[1]), int(pixel4[1]), G[0]), \
                     max(math.ceil(pixel[1]), math.ceil(pixel2[1]), math.ceil(pixel3[1]), math.ceil(pixel4[1]), G[1])
        R[0], R[1] = min(int(pixel[2]), int(pixel2[2]), int(pixel3[2]), int(pixel4[2]), R[0]), \
                     max(math.ceil(pixel[2]), math.ceil(pixel2[2]), math.ceil(pixel3[2]), math.ceil(pixel4[2]), R[1])

print(B, G, R)
for i in range(w):
    for j in range(h):
        pixel = img[i][j]
        if B[0] <= pixel[0] <= B[1] and G[0] <= pixel[1] <= G[1] and R[0] <= pixel[2] <= R[1]:
            img[i][j] = [0, 0, 0]

cv2.imshow("New Image", img)
cv2.waitKey(0)
cv2.imwrite('template.png', img)