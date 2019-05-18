import json
import sys
import os
from shutil import copyfile

file_name = 'data.json'
file = open(file_name,'r')
data = json.load(file)

shapes = ['capsule', 'diamond', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

color_folder = './colors/'
images_folder = './images/full/'
colors = ["white", "gray", "pink", "brown", "blue", "yellow", "green", "orange", "red", "purple", "turquoise", "black"]
for c in colors:
    os.mkdir(color_folder + c + '/')
for shape in data:
    if shape not in shapes: continue
    for name,shape_data in data[shape]['data'].items():
        try:
            color = shape_data.get('color', None)
            if ',' in color: continue
            c = color.lower()
            s = name[4:]
            s_folder = images_folder + s + '/'
            copyfile(s_folder + name + '.png', color_folder + c + '/' + name + '.png')
        except Exception as e:
            continue
