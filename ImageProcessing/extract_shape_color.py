import imutils
import cv2
import numpy as np
from collections import OrderedDict
from scipy.spatial import distance as dist
from PIL import Image
import os
import sys

def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)


def detect(c):
    # initialize the shape name and approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)
    if len(approx) == 3:
        shape = "triangle"
    elif len(approx) == 4:
        # compute the bounding box of the contour and use it to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        # a square will have an aspect ratio that is approximately equal to one
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    elif len(approx) == 5:
        shape = "pentagon"
    elif 6 < len(approx) <15:
        shape = "elipse"
    else:
        shape = "circle"

    return shape


def label(image,c):
    file = open('color.txt', 'r')
    l = file.readlines()
    col = [x.split(':')[0].strip() for x in l]
    rgb = []
    for x in l:
        line = x.split(':')[1].strip().split(',')
        rgb.append((int(line[0][1:]), int(line[1]), int(line[2][:-1])))
    colors = dict(zip(col, rgb))
    # allocate memory for the L*a*b* image, then initialize color names list
    lab = np.zeros((len(colors), 1, 3), dtype="uint8")
    colorNames = []

    for (i, (name, rgb)) in enumerate(colors.items()):
        # update the L*a*b* array and the color names list
        lab[i] = rgb
        colorNames.append(name)

    # convert the L*a*b* array from the RGB color space to L*a*b*
    lab = cv2.cvtColor(lab, cv2.COLOR_RGB2LAB)

    # construct a mask for the contour, then compute the average L*a*b* value for the masked region
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    mask = cv2.erode(mask, None, iterations=2)
    mean = cv2.mean(image, mask=mask)[:3]

    # initialize the minimum distance found thus far
    minDist = (np.inf, None)

    # loop over the known L*a*b* color values
    for (i, row) in enumerate(lab):
        # compute the distance between the current L*a*b* color value and the mean of the image
        d = dist.euclidean(row[0], mean)
        # if the distance is smaller than the current distance, then update the bookkeeping variable
        if d < minDist[0]:
            minDist = (d, i)

    # return the name of the color with the smallest distance
    return colorNames[minDist[1]]


image = cv2.imread(sys.argv[1])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
# ratio = 1
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)[1]
# thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
# display("Image", image)
# display("Gray", gray)
# display("Thresh", thresh)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

all = ""
for c in cnts:
    shape = detect(c)
    color = label(lab, c)
    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape and labeled
    # color on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    text = "{} {}".format(color, shape)
    all += text + "\n"
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
# display("Final Image", image)
cv2.imwrite('extract_shape_color_img.jpg', image)
open("extract_shape_color_txt.txt", 'w').write(all)
