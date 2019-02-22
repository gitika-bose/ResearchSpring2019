import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt

def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

img2 = cv2.imread(sys.argv[1])
# display("Original", img2)
img = img2.copy()
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (1,1,img.shape[1]-1,img.shape[0]-1)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
# display("Image", img)
cv2.imwrite('grabcut_img.jpg', img)
# plt.imshow(img),plt.colorbar(),plt.show()

