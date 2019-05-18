import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
from scipy.spatial import distance as dist

# Reference for visualization of image:
def clustering(input_file):
    im = Image.open(input_file).convert('RGB')
    pixels = list(im.getdata())
    pixels = [(x/255, y/255, z/255) for (x,y,z) in pixels]

    # c is the number of clusters
    c = 3
    cluster = KMeans(n_clusters=c).fit(pixels)
    colors = cluster.cluster_centers_ # the cluster centers are the dominant colors
    predictions = cluster.predict(pixels)
    freq = {}
    for l in predictions:
        ll = tuple(colors[l])
        if ll in freq: freq[ll] += 1
        else: freq[ll] = 1
    color_rgb = [(x*255, y*255, z*255) for [x,y,z] in colors]

    f = open("color.txt", "r")
    color_values = [tuple((i.split(":")[0], eval(i.split(" ")[1]))) for i in (f.read()).split("\n")]
    f.close()

    # REMOVES BLACK
    for j in color_rgb:
        minDist = (np.inf, None)
        for (i, row) in enumerate(color_values):
            # compute the distance between the current L*a*b* color value and the mean of the image
            d = dist.euclidean(row[1], j)
            # if the distance is smaller than the current distance, then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, row[0])

        if minDist[1] == 'Black':
            check = (j[0]/255, j[1]/255, j[2]/255 )

            if check in freq:
                del freq[check]
            color_rgb.remove(j)
            break

    colors = ["blue", "brown", "gray", "green", "orange", "purple", "pink", "red", "turquoise", "white", "yellow"]
    # GETS ALL COLORS
    color_values = {"blue":[], "brown":[], "gray":[], "green":[], "orange":[], "purple":[], "pink":[], "red":[], "turquoise":[], "white":[], "yellow":[]}
    for color in colors:
        f2 = open(color + ".txt", "r")
        for i in f2: color_values[color].append(eval(i))
        f2.close()


    # CLASSIFY EACH COLOR
    classified = []
    for c in color_rgb:
        check = (c[0] / 255, c[1] / 255, c[2] / 255)
        all = []
        for color in colors:
            for i in color_values[color]:
                if i:
                    d = dist.euclidean(c, i)
                    all.append((d,color))
        all.sort(key=lambda x: x[0])
        all = all[:5]
        final = {}
        for i in all:
            if i[1] in final:
                final[i[1]][0] += 1
                final[i[1]][1] += -i[0]
            else:
                final[i[1]] = [1, -i[0], i[1]]

        final = list(final.values())
        final.sort(key=lambda x: (x[0], x[1]), reverse=True)

        if final[0][2] not in classified: classified.append(final[0][2])

        if check in freq:
            freq[final[0][2]] = freq[check]
            del freq[check]

    if len(classified) > 1:
        if freq[classified[0]] <= 0.50*freq[classified[1]]:
            del classified[0]
        elif freq[classified[1]] <= 0.50*freq[classified[0]]:
            del classified[1]


    return classified



# print(clustering("pill_shapes/capsule/capsule-front_grabcut.jpg"))
print(clustering("../post_images/grabcut_img.jpg"))

