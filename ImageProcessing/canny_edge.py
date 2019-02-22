import cv2
import sys

imagepath = sys.argv[1]
img = cv2.imread(imagepath)

cv2.imshow("Original", img)
cv2.namedWindow('bar')
cv2.createTrackbar('min','bar',0,255,lambda x:x)
cv2.createTrackbar('max','bar',0,255,lambda x:x)

while (1):
    min=cv2.getTrackbarPos('min','bar')
    max=cv2.getTrackbarPos('max','bar')
    edges = cv2.Canny(img,min,max)
    cv2.imshow("Original", img)
    cv2.imshow("Edges", edges)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
