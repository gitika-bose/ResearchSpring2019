import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

shapes = ['bullet', 'capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

img = cv2.imread('White.jpg',0)
img = imutils.resize(img, width=300)
img2 = img.copy()
for shape in shapes:
    print(shape)
    template = cv2.imread('templates/'+shape+'.png',0)
    template = img = imutils.resize(template, width=300)
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    meth = 'cv2.TM_CCOEFF'
    # for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    threshold = 0.8
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        # Show the final image with the matched area.
    cv2.imshow('Detected', img)
    cv2.waitKey(0)