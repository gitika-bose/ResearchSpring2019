import json
from PIL import Image
import sys
from os import listdir
from os.path import isfile, join
import os


shapes = ['capsule', 'diamond', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

file_name = 'data.json'
file = open(file_name, 'r')
data = json.load(file)

letter = sys.argv[1]

files2 = []
if len(sys.argv)>2:
    for i in range(2,len(sys.argv)):
        letter_folder = sys.argv[i]+'_s/'
        for f in listdir(letter_folder):
            if (isfile(join(letter_folder, f)) and '.png' in f): files2.append(f)

folder = 'images/full/'
save_folder = letter+'_s/'
if not os.path.exists(save_folder): os.makedirs(save_folder)

let = []
for shape in shapes:
    shape_data = data[shape]['data']
    annotation_folder = folder + shape + '/annotations/'
    files = [f for f in listdir(annotation_folder) if (isfile(join(annotation_folder, f)) and '.xml' in f)]
    for name in shape_data:
        imprint = shape_data[name].get('imprint',None)
        try:
            if imprint:
                if letter in imprint:
                    if name+'.xml' not in files and name+'.png' not in files2:
                        let.append(name)
                        file = folder + shape + '/' + name + '.png'
                        img = Image.open(file)
                        img.save(save_folder+name+'.png', 'PNG')
        except Exception as e:
            print(e)
            continue
