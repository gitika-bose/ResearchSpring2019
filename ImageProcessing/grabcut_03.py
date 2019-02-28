import numpy as np
import cv2
import sys
import imutils
from matplotlib import pyplot as plt

def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

shape = sys.argv[1]
type = sys.argv[2]
imagepath = 'pill_shapes/' + shape + '/' + shape + '_' + type + '.jpg'
folder = 'pill_shapes/' + shape + '/'
img2 = cv2.imread(imagepath)

# display("Original", img2)
img = img2.copy()
height,width = img.shape[:2]
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (5,5,img.shape[1]-5,img.shape[0]-5)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

# h,w = img.shape[:2]
# cnt = set()
# for i in range(h):
#     for j in range(w):
#         pixel = img[i][j]
#         if pixel == [0,0,0]:
#             up = img[i-1][j] if i-1 >=0 else None
#             down = img[i+1][j] if i+1 <h else None
#             left = img[i][j] if j-1 >=0 else None
#             right = img[i][j] if j-1 >=0 else None



        # if img[i][j][0] == 255 and img[i][j][1] == 255 and img[i][j][2] == 255:
        #
        #     continue
        # else:
        #     template[i][j][0],template[i][j][1],template[i][j][2] = 0,0,0



# img[np.where((img==[0,0,0]).all(axis=2))] = [255,255,255]
# mean = np.mean(img)
# img[img <= mean] = 0
#
# blurred = cv2.GaussianBlur(img, (5, 5), 0)
# gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
# lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
# thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)[1]
#
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
#
# final = []
# for c in cnts:
#     if len(final)==0:
#         final = c
#     elif len(c) > len(final):
#         final = c
#
# x, y, w, h = cv2.boundingRect(final)
# # print(x,y)
#
# white = np.zeros((h+5,w+5),np.uint8)
# white[white == 0] = 255
#
# x_n = [c[0][0]-x+3 for c in final]
# y_n = [c[0][1]-y+3 for c in final]
# arr = [[x_n[i], y_n[i]] for i in range(len(x_n))]
#
# ctr = np.array(arr).reshape((-1,1,2)).astype(np.int32)
# cv2.drawContours(white, [ctr], -1, (0, 0, 0), 8)
#
#
#
# # display("White", white)
# # display("Image", img)
# cv2.imwrite(folder+shape+'-front_extract.jpg', white)
# cv2.imwrite(folder+shape+'-front_grabcut.jpg', img)

