import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
from scipy.spatial import distance as dist

# Reference for visualization of image:
def clustering(input_file):

   im = Image.open(input_file).convert('RGB')
   h, w = im.size
   pixels = list(im.getdata())
   pixels = [(x/255, y/255, z/255) for (x,y,z) in pixels]

   # c is the number of clusters
   c = 3
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
   plt.imshow(new_img)
   plt.show()
   # color_rgb = [(x*255, y*255, z*255) for [x,y,z] in colors]
   # print(color_rgb)

# clustering("../images/pill_shapes/hexagon/hexagon-front_grabcut.jpg")
# clustering("./post_images/grabcut_img.jpg")
clustering("./post_images/grabcut_img.jpg")



# uses the cluster centers to predict the color of all pixels
# predictions = cluster.predict(pixels)
#
# height, width = im.size

# Creates a new image with the predictions from clustering
# d = colors.shape[1]
# new_image = np.zeros((width, height, d))
# l = 0
# for i in range(width):
#     for j in range(height):
#         new_image[i][j] = colors[predictions[l]]
#         l += 1