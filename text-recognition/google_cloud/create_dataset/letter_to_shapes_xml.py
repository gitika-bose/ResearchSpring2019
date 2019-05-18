from os import listdir
from os.path import isfile, join
import sys
from shutil import copyfile

shapes = ['capsule', 'diamond', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
letter = sys.argv[1]

folder = letter+'_s/annotations/'
files = [f for f in listdir(folder) if (isfile(join(folder, f)) and '.xml' in f)]
annotations_folder = 'images/full/{}/annotations/'

for file in files:
    name = file.split('.')[0]
    shape = name[4:]
    src = folder + file
    dst = annotations_folder.format(shape) + file
    copyfile(src, dst)