import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy.ndimage import label
import imutils
import sys


def show_image(name, img, vf = False):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    if vf:
        plt.imshow(img),plt.colorbar(),plt.show()

img = cv2.imread(sys.argv[1])
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# show_image('Imagem Inicial', img, True)

# https://stackoverflow.com/questions/44752240/how-to-remove-shadow-from-scanned-images-using-opencv
dilated_img = cv2.dilate(img, np.ones((13,13), np.uint8))
show_image('Dilated', dilated_img)

# bg_img = cv2.medianBlur(dilated_img, 7)
# show_image('Median Blur', bg_img)
#
# diff_img = 255 - cv2.absdiff(img, bg_img)
# show_image('Diff', diff_img)

_, img_bin = cv2.threshold(diff_img, 128, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
show_image('Bin1', img_bin)
cv2.imwrite('shadow.py', img_bin)
