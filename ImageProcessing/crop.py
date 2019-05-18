import cv2
import sys

img = cv2.imread(sys.argv[1], 0)

ret, thresh = cv2.threshold(img, 127, 255, 0)

contours, hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]

x, y, w, h  = cv2.boundingRect(cnt)

foreground = img[y:y+h, x:x+w]

cv2.imwrite("foreground.png", foreground)