import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1])
cv2.imshow("Original image",img)

# img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
# cv2.imshow(" image",img)
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=45., tileGridSize=(8,8))

lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
l, a, b = cv2.split(lab)  # split on 3 different channels

l2 = clahe.apply(l)  # apply CLAHE to the L-channel

lab = cv2.merge((l2,a,b))  # merge channels
img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
cv2.imshow('Increased contrast', img2)

dst = cv2.fastNlMeansDenoisingColored(img2,None,12,12,7,21)
cv2.imshow(' contrast', dst)

# cv2.imwrite('sunset_modified.jpg', img2)

def display(name, img):
   cv2.imshow(name, img)
   cv2.waitKey(0)

def LAB_delta(delta, img):
   h, w = img.shape[:2]
   for i in range(h):
       for j in range(w):
           img[i][j][0] += delta
   # return img

img = img2.copy()
# img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# LAB_delta(80,img)

height, width = img.shape[:2]
mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (5, 5, img.shape[1] - 5, img.shape[0] - 5)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask2[:, :, np.newaxis]
cv2.imshow('grabcut', img)

Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 2
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

cv2.imshow('res2',res2)
cv2.imwrite('trial_5.jpg', res2)
cv2.waitKey(0)
cv2.destroyAllWindows()