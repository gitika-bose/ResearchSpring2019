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
h, w = img.shape[:2]
# print(w, h)
wi, hi = 50, 50
# template = img[:wi, :hi] # top left
# template2 = img[w-wi:, h-hi:] # bottom right
# template3 = img[w-wi:, :hi] # top right
# template4 = img[:wi, h-hi:] # bottom left
w_c, h_c = int(w/2), int(h/2)

template = img[(h_c-int(hi/2)):(h_c+int(hi/2)), w_c+10:(w_c+wi+10)] #right
template2 = img[(h_c-int(hi/2)):(h_c+int(hi/2)), (w_c-wi-10):w_c-10] #left
# display("Template", template)
# display("Template", template2)

# B, G, R = set(), set(), set()s
# B_2, G_2, R_2 = set(), set(), set()
B, G, R = [300,0], [300,0], [300,0]
B_2, G_2, R_2 = [300,0], [300,0], [300,0]

# bgr = set()
for i in range(wi):
    for j in range(hi):
        pixel = template[i][j]
        pixel2 = template2[i][j]

        B[0], B[1] = min(int(pixel[0]), B[0]), max(math.ceil(pixel[0]), B[1])
        G[0], G[1] = min(int(pixel[1]), G[0]), max(math.ceil(pixel[1]), G[1])
        R[0], R[1] = min(int(pixel[2]), R[0]), max(math.ceil(pixel[2]), R[1])

        B_2[0], B_2[1] = min(int(pixel2[0]), B_2[0]), max(math.ceil(pixel2[0]), B_2[1])
        G_2[0], G_2[1] = min(int(pixel2[1]), G_2[0]), max(math.ceil(pixel2[1]), G_2[1])
        R_2[0], R_2[1] = min(int(pixel2[2]), R_2[0]), max(math.ceil(pixel2[2]), R_2[1])

        # print(pixel)
        # B.update([pixel[0], pixel[0]+2, pixel[0]-2])
        # G.update([pixel[1], pixel[1]+2, pixel[1]-2])
        # R.update([pixel[2],  pixel[2]+2,  pixel[2]-2])

        # B_2.update([pixel2[0], pixel2[0] + 2,  pixel2[0] - 2])
        # G_2.update([pixel2[1], pixel2[1] + 2, pixel2[1] - 2])
        # R_2.update([pixel2[2], pixel2[2] + 2, pixel2[2] - 2])

# sB, sG, sR = math.ceil(np.std(B)), math.ceil(np.std(G)), math.ceil(np.std(R))
# mB, mG, mR = int(np.mean(B)), int(np.mean(G)), int(np.mean(R))
# sB, sG, sR = np.std(B), np.std(G), np.std(R)
# mB, mG, mR = np.mean(B), np.mean(G), np.mean(R)
# print(mB, sB)
# print(mG, sG)
# print(mR, sR)
d = 10
B[0],G[0],R[0] = B[0]-d,G[0]-d,R[0]-d
B[1],G[1],R[1] = B[1]+d,G[1]+d,R[1]+d
B_2[0],G_2[0],R_2[0] = B_2[0]-d,G_2[0]-d,R_2[0]-d
B_2[1],G_2[1],R_2[1] = B_2[1]+d,G_2[1]+d,R_2[1]+d
for i in range(h):
    for j in range(w):
        pixel = img[i][j]
        if B[0] <= pixel[0] <= B[1] and G[0] <= pixel[1] <= G[1] and R[0] <= pixel[2] <= R[1] or \
                B_2[0] <= pixel[0] <= B_2[1] and G_2[0] <= pixel[1] <= G_2[1] and R_2[0] <= pixel[2] <= R_2[1]:
            continue
        else:
            img[i][j] = [0, 0, 0]


        # if pixel[0] not in B and pixel[1] not in G and pixel[2] not in R:
        #     if pixel[0] not in B_2 and pixel[1] not in G_2 and pixel[2] not in R_2:
        #         img[i][j] = [0, 0, 0]
        # if tuple(pixel) not in bgr:
        #     img[i][j] = [0, 0, 0]
        # if abs(pixel[0]-mB) <= sB and abs(pixel[1]-mG) <= sG and abs(pixel[2]-mR) <= sR:
        #     img[i][j] = [0, 0, 0]

# display("New Image", img)
cv2.imwrite('center.jpg', img)