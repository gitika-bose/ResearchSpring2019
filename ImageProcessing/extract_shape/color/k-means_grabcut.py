import numpy as np
import cv2
import sys
import imutils
from sklearn.cluster import KMeans
from PIL import Image
import os
from scipy.spatial import distance as dist

def clustering(pixels):
    # im = Image.open(input_file).convert('RGB')
    # pixels = list(im.getdata())
    # pixels = [(x / 255, y / 255, z / 255) for (x, y, z) in pixels]

    # c is the number of clusters
    c = 3
    cluster = KMeans(n_clusters=c).fit(pixels)
    colors = cluster.cluster_centers_  # the cluster centers are the dominant colors
    predictions = cluster.predict(pixels)
    freq = {}
    for l in predictions:
        ll = tuple(colors[l])
        if ll in freq:
            freq[ll] += 1
        else:
            freq[ll] = 1
    color_rgb = [(x * 255, y * 255, z * 255) for [x, y, z] in colors]

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
            check = (j[0] / 255, j[1] / 255, j[2] / 255)

            if check in freq:
                del freq[check]
            color_rgb.remove(j)
            break
    print(color_rgb)
    # color_dist = {'blue': [38.67909323385706, 83.17539551724416, 99.72995076050148], 'brown': [180.66397792141726, 156.92612615117238, 129.07029803603848],
    #               'gray': [38.67909323385706, 83.17539551724416, 99.72995076050148], 'green': [76.30433240255222, 158.73343583270093, 172.78465877511002],
    #               'orange': [180.66397792141726, 156.92612615117238, 129.07029803603848], 'purple': [144.86124764258298, 87.61971110616834, 66.19199789229614],
    #               'pink': [167.15212990361707, 121.58382162803022, 109.28136148106313], 'red': [109.9024540423136, 43.26438240653532, 34.92494044858991],
    #               'turquoise': [76.30433240255222, 158.73343583270093, 172.78465877511002], 'white': [189.73095659253966, 188.66612848876662, 185.0022331302897],
    #               'yellow': [180.66397792141726, 156.92612615117238, 129.07029803603848]}
    #
    # for c in color_rgb:
    #     check = (c[0] / 255, c[1] / 255, c[2] / 255)
    #     all = []
    #     for color in color_dist:
    #         print(check, tuple((color_dist[color][0]/255,color_dist[color][1]/255, color_dist[color][2]/25)))
    #         d = dist.euclidean(c, tuple((color_dist[color][0]/255,color_dist[color][1]/255, color_dist[color][2]/25)))
    #         all.append((d, color))
    #     all.sort(key=lambda x: x[0])
    #     print(all[:1])
    colors = ["blue", "brown", "gray", "green", "orange", "purple", "pink", "red", "turquoise", "white", "yellow"]
    # GETS ALL COLORS
    color_values = {"blue": [], "brown": [], "gray": [], "green": [], "orange": [], "purple": [], "pink": [], "red": [],
                    "turquoise": [], "white": [], "yellow": []}
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
                    all.append((d, color))
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

        if final[0][2] not in classified: classified.append((final[0][2],c))

        if check in freq:
            freq[final[0][2]] = freq[check]
            del freq[check]

    if len(classified) > 1:
        if freq[classified[0][0]] <= 0.50 * freq[classified[1][0]]:
            del classified[0]
        elif freq[classified[1][0]] <= 0.50 * freq[classified[0][0]]:
            del classified[1]

    return classified


to_display = False
def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

img2 = cv2.imread(sys.argv[1])
img = img2.copy()
h,w = img.shape[:2]

# Grabcut
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (5,5,img.shape[1]-5,img.shape[0]-5)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
if to_display: display('First Grabcut',img)

# Normalizing and making a list
pixels = []
for i in range(h):
    for j in range(w): pixels.append(img[i][j]/255)

# K-Means
c = 4
cluster = KMeans(n_clusters=c).fit(pixels)
labels = cluster.predict(pixels)
colors = cluster.cluster_centers_
new_img = np.zeros((h, w, 3))
counter = 0
for i in range(h):
    for j in range(w):
        new_img[i][j] = colors[labels[counter]]
        counter += 1
if to_display: display('K-Means-pre',new_img)

# K-Means Post Processing
edge_pixels = {}
w_in = [x for x in range(5,w-5)]
h_in = [x for x in range(5,h-5)]
for i in range(h):
    for j in range(w):
        if i not in h_in:
            if tuple(new_img[i][j]) not in edge_pixels: edge_pixels[tuple(new_img[i][j])] = 0
            edge_pixels[tuple(new_img[i][j])] += 1
        if j not in w_in:
            if tuple(new_img[i][j]) not in edge_pixels: edge_pixels[tuple(new_img[i][j])] = 0
            edge_pixels[tuple(new_img[i][j])] += 1

to_delete = [e for e in edge_pixels if edge_pixels[e]<500]
for t in to_delete: del edge_pixels[t]
edge_pixels = set(edge_pixels.keys())
for i in range(h):
    for j in range(w):
        if tuple(new_img[i][j]) in edge_pixels:
            new_img[i][j] = [0,0,0]
if to_display: display('K-Means-post',new_img)

# temp_image = new_img * 255
# temp_image = temp_image.astype(np.uint8)
# cv2.imwrite('Boop.jpg',temp_image)
pixels = []
for i in range(h):
    for j in range(w): pixels.append(img[i][j][::-1]/255)
# for c in colors:
#     print(c,c*255)
# exit()
print(clustering(pixels))
exit()

# Grabcut
img = new_img * 255
img = img.astype(np.uint8)
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (5,5,img.shape[1]-5,img.shape[0]-5)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

# Grabcut Post-Processing
img[np.where((img!=[0,0,0]).all(axis=2))] = [255,255,255]
blurred = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
final = []
for c in cnts:
    if len(final)==0:
        final = c
    elif len(c) > len(final):
        final = c

x, y, w, h = cv2.boundingRect(final)
white = np.zeros((h+5,w+5),np.uint8)
white[white == 0] = 255
x_n = [c[0][0]-x+3 for c in final]
y_n = [c[0][1]-y+3 for c in final]
arr = [[x_n[i], y_n[i]] for i in range(len(x_n))]
ctr = np.array(arr).reshape((-1,1,2)).astype(np.int32)
cv2.drawContours(white, [ctr], -1, (0, 0, 0), 8)

if to_display: display('Original',img2)
if to_display: display('Grabcut',img)
if to_display: display('Border',white)

# Storing Image temporarily to make it an actual (3-D) image
cv2.imwrite('temp.jpg',white)
white = cv2.imread('temp.jpg')

# Comparing against templates
shapes = ['bullet', 'capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
template_folder = './templates/'
img = imutils.resize(white, width=300)
h,w = img.shape[:2]
compare = []
for shape in shapes:
    temp = cv2.imread(template_folder+shape+'.png')
    template = temp.copy()

    template = imutils.resize(template, width=300)
    h_t, w_t = template.shape[:2]
    for i in range(h_t):
        for j in range(w_t):
            if template[i][j][0] == 0 and template[i][j][1] == 0 and template[i][j][2] == 0:
                template[i][j][0], template[i][j][1], template[i][j][2] = 255, 255, 255
            elif template[i][j][0] == 255 and template[i][j][1] == 255 and template[i][j][2] == 255: continue
            else: template[i][j][0], template[i][j][1], template[i][j][2] = 0, 0, 0
    if h >= h_t*2 or h_t >= h*2:
        compare.append((99999999,shape))
    else:
        w_i, h_i = min(w,w_t), min(h,h_t)
        # print(w_i,h_i)
        final = img[:h_i,:w_i] - template[:h_i,:w_i]
        whites = np.sum(final == 255)
        compare.append((whites, shape))
compare.sort(key=lambda x:x[0])
compare = [x for x in compare if x[0]!=99999999]
if to_display: print(compare)

os.remove('temp.jpg')