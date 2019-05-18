from PIL import Image
import json
from os import listdir
from os.path import isfile, join
import numpy as np

def num_to_file(count):
    count = int(count)
    if count < 10: return '000'+str(count)
    elif count <100: return '00'+str(count)
    elif count <1000: return '0'+str(count)
    else: return str(count)

# shapes = ['bullet','capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
#           'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
# shapes = ['bullet']
# names = ['0021', '']
# folder1 = 'images/full/'
#
# file_name = 'data.json'
# file = open(file_name, 'r')
# data = json.load(file)

# # Crop 1
# shape = 'round'
# additional = ''
# folder_root = 'images/full/'
# folder = folder_root + shape + '/' + additional
# files = [f for f in listdir(folder) if isfile(join(folder, f))]
#
# for file_name in files:
#     file = file_name.split('.')[0]
#     if file:
#         file = folder + file
#         img = Image.open(file+'.png')
#         width, height = img.size
#         remove = (0, 0, width, height-115)
#         new_img2 = img.crop(remove)
#         new_img2.save(file+'.png', 'PNG')

# Crop 2
shape = 'oval'
in_folder = ''
folder_root = 'images/full/'
folder = folder_root + in_folder + shape + '/'
images = [num_to_file(x)+shape for x in range(346, 1477)]

for image in images:
    check=True
    file = folder+image
    img = Image.open(file+'.png')
    width, height = img.size
    data = np.array(img.getdata()).reshape((height, width, 3))
    for d in range(len(data[0])):
        arr = data[:,d]
        count = 0
        for a in arr:
            if a[0] == 204 and a[1] == 204 and a[2] == 204: count +=1
        if count >= height//2:
            check = False
            remove = (d+2,0,width,height)
            new_img2 = img.crop(remove)
            new_img2.save(file + '.png', 'PNG')
            break
    if check: print(image)
        #         new_img2.save(file+'.png', 'PNG')
# data2, count = [], 0
# for i in height:
#     n = []
#     for j in width:
#         n.append(data[count])
#         count+=1
#     data2.append()





