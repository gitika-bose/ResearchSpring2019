"""
Before start:
export GOOGLE_APPLICATION_CREDENTIALS=helper_files/research-pill-google_service_account_key.json
export PROJECT_ID=research-pill
"""
import sys
import json
from google.cloud import automl_v1beta1
import numpy as np
import cv2
import imutils
from sklearn.cluster import KMeans
import os
from scipy.spatial import distance as dist
import time
from PIL import Image, ImageDraw


debug = False
debug_display = False
write_images = False
def display(name,img,convert=False):
    img_cp = img.copy()
    if convert:
        img_cp = img_cp * 255
        img_cp = img_cp.astype(np.uint8)
    cv2.imshow(name,img_cp)
    cv2.waitKey(0)

def write_exit(name,img,convert=False):
    if convert:
        img_cp = img.copy()
        img_cp = img_cp*255
        img_cp = img_cp.astype(np.uint8)
        cv2.imwrite('pictures/' + name + '.jpg', img_cp)
    else: cv2.imwrite(name+'.jpg',img)
    exit()

def write(name,img,convert=False):
    if convert:
        img_cp = img.copy()
        img_cp = img_cp*255
        img_cp = img_cp.astype(np.uint8)
        cv2.imwrite('pictures/yellow_pill/' + name + '.jpg', img_cp)
    else: cv2.imwrite('pictures/yellow_pill/' + name+'.jpg',img)

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def clustering(pixels,h,w):
    c = 3
    cluster = KMeans(n_clusters=c).fit(pixels)
    colors = cluster.cluster_centers_  # the cluster centers are the dominant colors
    predictions = cluster.predict(pixels)

    new_img = np.zeros((h, w, 3))
    counter = 0
    for i in range(h):
        for j in range(w):
            new_img[i][j] = colors[predictions[counter]][::-1]
            counter += 1
    if debug_display: display('K-Means-Color', new_img, convert=True)
    if write_images: write('K-Means-Color',new_img,convert=True)

    freq = {}
    for l in predictions:
        ll = tuple(colors[l])
        if ll in freq: freq[ll] += 1
        else: freq[ll] = 1
    color_rgb = [(x * 255, y * 255, z * 255) for [x, y, z] in colors]

    f = open("helper_files/color.txt", "r")
    color_values = [tuple((i.split(":")[0], eval(i.split(" ")[1]))) for i in (f.read()).split("\n")]
    f.close()

    for j in color_rgb:
        minDist = (np.inf, None)
        for (i, row) in enumerate(color_values):
            d = dist.euclidean(row[1], j)
            if d < minDist[0]: minDist = (d, row[0])

        if minDist[1] == 'Black':
            check = (j[0] / 255, j[1] / 255, j[2] / 255)
            if check in freq: del freq[check]
            color_rgb.remove(j)
            break

    colors = ["blue", "brown", "gray", "green", "orange", "purple", "pink", "red", "turquoise", "white", "yellow"]
    color_values = {"blue": [], "brown": [], "gray": [], "green": [], "orange": [], "purple": [], "pink": [], "red": [],
                    "turquoise": [], "white": [], "yellow": []}
    for color in colors:
        f2 = open('helper_files/' + color + ".txt", "r")
        for i in f2: color_values[color].append(eval(i))
        f2.close()

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
            else: final[i[1]] = [1, -i[0], i[1]]

        final = list(final.values())
        final.sort(key=lambda x: (x[0], x[1]), reverse=True)
        if final[0][2] not in classified: classified.append((final[0][2],c))
        if check in freq:
            freq[final[0][2]] = freq[check]
            del freq[check]

    if len(classified) > 1:
        if freq[classified[0][0]] <= 0.75 * freq[classified[1][0]]: del classified[0]
        elif freq[classified[1][0]] <= 0.75 * freq[classified[0][0]]: del classified[1]
    return classified

img2 = cv2.imread(sys.argv[1])
if debug_display: display('Original',img2)
img = img2.copy()
img3 = img2.copy()
h,w = img.shape[:2]

# Grabcut
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (5,5,img.shape[1]-5,img.shape[0]-5)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
if debug_display: display('first_grabcut',img)
if write_images: write('first_grabcut',img)

# Output Color
pixels = []
for i in range(h):
    for j in range(w): pixels.append(img[i][j][::-1]/255)
color_output = list(set(col[0] for col in clustering(pixels,h,w)))
print('Color: ', color_output)

# K-Means
pixels = []
for i in range(h):
    for j in range(w): pixels.append(img[i][j]/255)
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
if debug_display: display('K-Means-pre',new_img)
if write_images: write('K-Means-pre',new_img, convert=True)

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
if debug_display: display('K-Means-post',new_img)
if write_images: write('K-Means-post',new_img, convert=True)

img = new_img * 255
img = img.astype(np.uint8)

# Contour Extraction
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
if debug_display: display('Outline',white)
if write_images: write('Outline',white)

# Storing Image temporarily to make it an actual (3-D) image
cv2.imwrite('temp.jpg',white)
white = cv2.imread('temp.jpg')

# Comparing against templates
shapes = ['bullet', 'capsule', 'diamond', 'double-circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
groups = [['capsule', 'diamond', 'double-circle', 'oval', 'tear', 'trapezoid'], ['hexagon', 'pentagon', 'round', 'semi-circle', 'square', 'trapezoid', 'triangle'], ['octagon', 'rectangle', 'semi-circle'], ['freeform'], ['bullet']]
probability = {'round': 2032, 'oval': 1476, 'capsule': 738, 'triangle': 30, 'rectangle': 27, 'diamond': 16, 'pentagon': 15, 'tear': 13, 'hexagon': 12, 'square': 12, 'bullet': 6, 'semi-circle': 5, 'trapezoid': 3, 'freeform': 2, 'octagon': 2, 'double-circle': 3}
template_folder = './templates/'
img = imutils.resize(white, width=300)
h,w = img.shape[:2]
compare,compare_dict,compare2 = [], {}, []
for shape in shapes:
    temp = cv2.imread(template_folder+shape+'.png')
    template = temp.copy()

    template = imutils.resize(template, width=300)
    h_t, w_t = template.shape[:2]
    if h >= h_t*2 or h_t >= h*2:
        compare.append((99999999,shape))
    else:
        w_i, h_i = min(w, w_t), min(h, h_t)
        result = mse(img[:h_i,:w_i],template[:h_i,:w_i])
        compare.append((result, shape))
        compare_dict[shape] = result
compare = [x for x in compare if x[0]!=99999999]
compare.sort(key=lambda x:x[0])
if debug: print('Shape Recog: Compare all 1', compare)
ans = compare[0][1]
for g in groups:
    if ans in g:
        for gg in g:
            if gg in compare_dict:
                result = compare_dict[gg] * (1-probability[gg]/4400)
                compare2.append((result,gg))
compare2.sort(key=lambda x:x[0])
compare = compare2
if debug: print('Shape Recog: Compare all 2', compare)
os.remove('temp.jpg')

imprint_json, data_json, color_json, shape_json = open('helper_files/imprints.json'), open('helper_files/data.json'), open('helper_files/colors.json'), open('helper_files/shapes.json')
imprints, colors, shapes = json.load(imprint_json), json.load(color_json), json.load(shape_json)
data = json.load(data_json)
links = open('links.txt','w')

# Output Shape
shapes_output = [compare[0][1]]
if 'oval' in shapes_output and 'capsule' not in shapes_output: shapes_output.append('capsule')
if 'capsule' in shapes_output and 'oval' not in shapes_output: shapes_output.append('oval')
print('Shape:', shapes_output)
pills_shapes = set()
for cc in shapes_output:
    if not pills_shapes: pills_shapes = set(shapes[cc])
    else: pills_shapes = pills_shapes.union(set(shapes[cc]))
if debug: print('Pills after shape: ', pills_shapes)

pills_color = set()
for cc in color_output:
    if not pills_color: pills_color = set(colors[cc])
    else: pills_color = pills_color.intersection(set(colors[cc]))
if debug: print('Pills after Color: ', pills_color)

# Shape and Color Intersection
pills = pills_shapes.intersection(pills_color)
if debug: print('Pills after shape and color: ', pills)

def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def resolve_y(res):
    result = {}
    bounds = []
    count = 0
    for r in res:
        ytop,ybot = r[2],r[4]
        check = True
        for b in bounds:
            s5 = 75*(b[1]-b[0])/100
            if b[0] <= ybot <= b[1] and b[0] <= ytop <= b[1] and (ybot-ytop) >= s5:
                result[b[2]].append(r)
                check = False
                break
            elif ybot >= b[1] and b[0] >= ytop and (ybot-ytop) >= s5:
                result[b[2]].append(r)
                b[0] = ytop
                b[1] = ybot
                check = False
                break
            elif b[0] <= ybot <= b[1] and (ybot-b[0]) >= s5:
                result[b[2]].append(r)
                b[0] = ytop
                check = False
                break
            elif b[0] <= ytop <= b[1] and (b[1]-ytop) >= s5:
                result[b[2]].append(r)
                b[1] = ybot
                check = False
                break
        if check:
            bounds.append([ytop, ybot, count])
            result[count] = [r]
            count += 1
    return [sorted(v,key=lambda x:x[1]) for k,v in result.items()]

def resolve_x(res):
    result = []
    for rr in res:
        bounds = []
        for r in rr:
            n, x1, x2 = r[0], r[1], r[3]
            check = True
            for b in bounds:
                b_n, b_x1, b_x2 = b[0], b[1], b[2]
                if abs(x1-b_x2) <= 0.05:
                    b[0] += n
                    b[2] = x2
                    check=False
                    break
            if check:
                bounds.append([r[0],r[1],r[3]])
        for b in bounds: result.append(b[0])
    return result

image_path = sys.argv[1]
project_id_letters, model_id_letters = 'research-pill', 'IOD8510123241962995712'
project_id_numbers, model_id_numbers = 'research-pill', 'IOD9124864591099068416'
pills_imprint, names2 = None, None
content = open(image_path, 'rb').read()
letters = get_prediction(content, project_id_letters, model_id_letters)
numbers = get_prediction(content, project_id_numbers, model_id_numbers)
names,res = [], []
for n in numbers.payload:
    boxes = n.image_object_detection.bounding_box.normalized_vertices
    res.append((n.display_name,boxes[0].x,boxes[0].y,boxes[1].x,boxes[1].y))
    names.append(n.display_name)
for l in letters.payload:
    boxes = l.image_object_detection.bounding_box.normalized_vertices
    res.append((l.display_name,boxes[0].x,boxes[0].y,boxes[1].x,boxes[1].y))
    names.append(l.display_name)

# img4 = Image.open(sys.argv[1])
# h,w = img2.shape[:2]
# draw = ImageDraw.Draw(img4)
# for r in res: draw.rectangle([r[1]*w,r[2]*h, r[3]*w, r[4]*h], outline=(0, 0, 0), width=1)
# img4.save('Imprint.png', "PNG")

res = resolve_y(res)
if debug: print('Imprint Recog: Resolve Y', res)
names2 = resolve_x(res)
if debug: print('Imprint Recog: Resolve X', names2)
for name in names:
    if not pills_imprint: pills_imprint = set(imprints[name])
    else: pills_imprint=pills_imprint.intersection(set(imprints[name]))
print('Imprint1: {}\nImprint2: {}'.format(names,names2))
if not names: print('Imprint is empty. Take better images')
if not names2: print('Imprint2 is empty. Precision can be improved')
if debug: print('Pills after imprint 1: ', pills_imprint)

final_pills = set()
if pills_imprint:
    for pill in pills_imprint:
        shape = pill[4:]
        shape_data = data[shape]['data'][pill]
        imprint = shape_data.get('imprint_list', None)
        if not imprint: imprint = [shape_data.get('imprint', None)]
        overall_check = True
        for name in names2:
            check = True
            for i in imprint:
                if name in i:
                    check = False
                    break
            if check:
                overall_check=False
                break
        if overall_check:
            if pill in pills:
                final_pills.add(pill)
                links.write(shape_data['imageUrl'] + '\n')
                print('Pill: {}, url: {}'.format(pill,shape_data['imageUrl']))

    if not final_pills:
        print('No Pill was found with Imprint2. Precision can be improved to get better imprint2 / the pill doesnt exist in the database.\nMore generic ones are:')
        for pill in pills_imprint:
            if pill in pills:
                shape = pill[4:]
                shape_data = data[shape]['data'][pill]
                final_pills.add(pill)
                links.write(shape_data['imageUrl'] + '\n')
                print('Pill: {}, url: {}'.format(pill, shape_data['imageUrl']))
else:
    print('No Imprint: Take new images.\nMore generic ones based on the shape and color are:')
    for pill in pills:
        shape = pill[4:]
        shape_data = data[shape]['data'][pill]
        final_pills.add(pill)
        links.write(shape_data['imageUrl'] + '\n')
        print('Pill: {}, url: {}'.format(pill, shape_data['imageUrl']))
