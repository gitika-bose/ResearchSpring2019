import cv2
import sys
import numpy as np

white = np.zeros((500,500,3),np.uint8)

cv2.namedWindow('bar')
cv2.createTrackbar('L','bar',0,100,lambda x:x)
cv2.createTrackbar('a','bar',0,255,lambda x:x)
cv2.createTrackbar('b','bar',0,255,lambda x:x)
while (1):
    L = cv2.getTrackbarPos('L','bar')
    a = cv2.getTrackbarPos('a','bar')-128
    b = cv2.getTrackbarPos('b','bar')-128
    white[np.where((white!=[400,400,400]).all(axis=2))] = [L,a,b]
    cv2.imshow("Edges", white)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
