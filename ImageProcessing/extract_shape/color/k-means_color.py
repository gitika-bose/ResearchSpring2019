import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
from scipy.spatial import distance as dist

# Reference for visualization of image:
def clustering(pixels):

   # c is the number of clusters
   c = 11
   cluster = KMeans(n_clusters=c).fit(pixels)

   # the cluster centers are the dominant colors
   labels = cluster.predict(pixels)
   colors = cluster.cluster_centers_
   # print(colors)
   color_dict = {}
   for i in range(len(pixels)):
      color_dict[pixels[i]] = list(colors[labels[i]])
   return color_dict
   # new_img = np.zeros((w, h, 3))
   # counter = 0
   # for i in range(w):
   #    for j in range(h):
   #       new_img[i][j] = colors[labels[counter]]
   #       counter += 1
   # plt.imshow(new_img)
   # plt.show()
   # color_rgb = [(x*255, y*255, z*255) for [x,y,z] in colors]
   # print(color_rgb)

all = set()
colors = ["blue", "brown", "gray", "green", "orange", "purple", "pink", "red", "turquoise", "white", "yellow"]
# GETS ALL COLORS
color_values = {"blue":[], "brown":[], "gray":[], "green":[], "orange":[], "purple":[], "pink":[], "red":[], "turquoise":[], "white":[], "yellow":[]}
for color in colors:
   f2 = open(color + ".txt", "r")
   for i in f2:
      all.add(eval(i))
      color_values[color].append(eval(i))
   f2.close()

# clustering("../images/pill_shapes/hexagon/hexagon-front_grabcut.jpg")
# clustering("./post_images/grabcut_img.jpg")
color_dict = clustering(list(all))
final = {}
for c in color_values:
   final[c] = color_dict[color_values[c][0]]
print(final)



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




#  73.18966927 157.84789532 172.17316896 -
# 181.41372432 157.97915743 129.84016101 -
# 167.30673924 123.56220495 110.7647393  -
# 110.97033814  44.59050921  34.96353677 -
# 190.0181722  188.98865004 185.35742809 -
# 169.71511607 169.75886403 168.07757934 -
# 145.34350394  87.43842668  69.99201502 -
# 190.71600627  57.44571778  26.69646765 -
# 180.94332949 130.00119898  58.84620505 -
#  37.96816966  83.23527368  99.82253726 -
# 117.85490966 140.7654103  145.41872598 -