# records different colors within the template (say 25 * 25 pixels)
# and check which pixel in the image is within the list of colors

import numpy as np
import cv2
import imutils
import math
import sys
import numpy as np

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
# display("template", template)

B, G, R = [300,-300], [300,-300], [300,-300]
# bgr = set()
for i in range(wi):
    for j in range(hi):
        # pixel = template[i][j]
        # pixel2 = template2[i][j]
        # pixel3 = template3[i][j]
        # pixel4 = template4[i][j]
        lab = np.zeros((4, 1, 3), dtype="uint8")
        lab[0] = template[i][j]
        lab[1] = template2[i][j]
        lab[2] = template3[i][j]
        lab[3] = template4[i][j]
        lab = cv2.cvtColor(lab, cv2.COLOR_RGB2LAB)
        pixel = np.asarray(lab[0])
        pixel2 = np.asarray(lab[1])
        pixel3 = np.asarray(lab[2])
        pixel4 = np.asarray(lab[3])

        B[0], B[1] = min(int(pixel[0]), int(pixel2[0]), int(pixel3[0]), int(pixel4[0]), B[0]), \
                     max(math.ceil(pixel[0]), math.ceil(pixel2[0]), math.ceil(pixel3[0]), math.ceil(pixel4[0]), B[1])
        G[0], G[1] = min(int(pixel[1]), int(pixel2[1]), int(pixel3[1]), int(pixel4[1]), G[0]), \
                     max(math.ceil(pixel[1]), math.ceil(pixel2[1]), math.ceil(pixel3[1]), math.ceil(pixel4[1]), G[1])
        R[0], R[1] = min(int(pixel[2]), int(pixel2[2]), int(pixel3[2]), int(pixel4[2]), R[0]), \
                     max(math.ceil(pixel[2]), math.ceil(pixel2[2]), math.ceil(pixel3[2]), math.ceil(pixel4[2]), R[1])

# print(B, G, R)
for i in range(w):
    for j in range(h):
        pixel = img[i][j]
        if B[0] <= pixel[0] <= B[1] and G[0] <= pixel[1] <= G[1] and R[0] <= pixel[2] <= R[1]:
            img[i][j] = [0, 0, 0]


blurred = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

final = []
for c in cnts:
    if len(final)==0:
        final = c
    elif len(c) > len(final):
        final = c

x, y, w, h = cv2.boundingRect(final)
# print(x,y)

white = np.zeros((h+5,w+5),np.uint8)
white[white == 0] = 255

x_n = [c[0][0]-x+3 for c in final]
y_n = [c[0][1]-y+3 for c in final]
arr = [[x_n[i], y_n[i]] for i in range(len(x_n))]

ctr = np.array(arr).reshape((-1,1,2)).astype(np.int32)
cv2.drawContours(white, [ctr], -1, (0, 0, 0), 8)

# display("White", white)
# display("Image", img)
cv2.imwrite('post_images/extract_background_own_02_white.jpg', white)
cv2.imwrite('post_images/extract_background_own_02_img.jpg', img)

# display("New Image", img)
# cv2.imwrite('post_images/extract_background_own_02_img.jpg', img)