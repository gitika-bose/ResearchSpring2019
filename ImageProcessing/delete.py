import os
import shutil

shapes = ['bullet', 'capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
main_folder = 'pill_shapes/'

for shape in shapes:
    folder = main_folder + shape + "/"
    compare = folder + shape + '-compare/'
    if os.path.isdir(compare):
        shutil.rmtree(compare)