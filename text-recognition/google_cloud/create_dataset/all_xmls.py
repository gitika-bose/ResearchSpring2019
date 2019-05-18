from os import listdir
from os.path import isfile, join, isdir
import os
from shutil import copyfile

root_folder = './images/full/'
copy_folder = './dataset/xmls/'
shapes = ['capsule', 'diamond', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
for shape in shapes:
    folder = root_folder + shape+'/annotations/'
    files = [f for f in listdir(folder) if (isfile(join(folder, f)) and '.xml' in f)]
    for f in files: copyfile(folder+f, copy_folder+f)


