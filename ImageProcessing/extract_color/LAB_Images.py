import cv2
import sys
import numpy as np

def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

imagepath = sys.argv[1]
img = cv2.imread(imagepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# display("Image",img)
h,w = img.shape[:2]
d = [x for x in range(0,110,10)]

for delta in d:
    img2 = img.copy()
    img3 = img.copy()
    for i in range(h):
        for j in range(w):
            img2[i][j][0] -= delta
            img3[i][j][0] += delta
    cv2.imwrite("post_images/LAB(-"+str(delta)+").jpg",img2)
    cv2.imwrite("post_images/LAB(+"+str(delta)+").jpg",img3)
