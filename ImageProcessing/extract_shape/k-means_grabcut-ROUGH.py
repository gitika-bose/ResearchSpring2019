import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
from scipy.spatial import distance as dist

def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

img2 = cv2.imread(sys.argv[1])
# display("Original", img2)
img = img2.copy()
w,h = img.shape[:2]
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (5,5,img.shape[1]-5,img.shape[0]-5)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

display('Grabcut',img)

pixels = []
for i in range(w):
    for j in range(h): pixels.append(img[i][j]/255)

# cv2.imwrite('post_images/grabcut_img.jpg', img)
# norm_image = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

# pixels = [nn for n in norm_image for nn in n]
# print(pixels)
#
c = 4
cluster = KMeans(n_clusters=c).fit(pixels)

# the cluster centers are the dominant colors
labels = cluster.predict(pixels)
colors = cluster.cluster_centers_

new_img = np.zeros((w, h, 3))
counter = 0
for i in range(w):
    for j in range(h):
        new_img[i][j] = colors[labels[counter]]
        counter += 1

# center_pixels = set()
# for i in range(w//2-20,w//2+21):
#     for j in range(h//2-20,h//2+21):
#         center_pixels.add(tuple(new_img[i][j]))
#
# for i in range(w):
#     for j in range(h):
#         if tuple(new_img[i][j]) not in center_pixels:
#             new_img[i][j] = [0,0,0]

edge_pixels = set()
w_in = [x for x in range(6,w-5)]
h_in = [x for x in range(6,h-5)]
for i in range(w):
    if i not in w_in:
        for j in range(h):
            if j not in h_in:
                edge_pixels.add(tuple(new_img[i][j]))

for i in range(w):
    for j in range(h):
        if tuple(new_img[i][j]) in edge_pixels:
            new_img[i][j] = [0,0,0]

# print(new_img)
display('Final',new_img)
plt.imsave('boop.jpg',new_img)

