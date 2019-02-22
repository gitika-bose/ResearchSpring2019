import numpy as np
import cv2
from matplotlib import pyplot as plt

img2 = cv2.imread('pill_images/pill_13_02.jpg')
cv2.imshow("Original",img2)
img = img2.copy()
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (1,1,img.shape[1]-1,img.shape[0]-1)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
cv2.imshow("image", img)
cv2.waitKey(0)
# plt.imshow(img),plt.colorbar(),plt.show()

