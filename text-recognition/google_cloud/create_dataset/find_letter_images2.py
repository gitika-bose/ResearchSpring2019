import json
from PIL import Image
import sys
from os import listdir
from os.path import isfile, join
import os
from shutil import copyfile


shapes = ['capsule', 'diamond', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

file_name = 'data.json'
file = open(file_name, 'r')
data = json.load(file)

letters = [chr(l) for l in range(65,91)] + [str(l) for l in range(0,10)]
# letters.remove('Q')
# letters = ['b','r','a','m','g','p','e','d']
# letters = ['b','B']
# letter = sys.argv[1]
for letter in letters:
    folder = 'images/full/'
    save_folder = 'dataset2/'+letter+'/'
    if not os.path.exists(save_folder): os.makedirs(save_folder)

    train, validate, test = save_folder+'train/', save_folder+'validate/', save_folder+'test/'
    if not os.path.exists(train): os.makedirs(train)
    if not os.path.exists(validate): os.makedirs(validate)
    if not os.path.exists(test): os.makedirs(test)

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
                        if name+'.xml' in files:
                            let.append(name)
                            src = folder + shape + '/' + name + '.png'
                            dst = save_folder+name+'.png'
                            copyfile(src, dst)
                            # img = Image.open(file)
                            # img.save(, 'PNG')
            except Exception as e:
                print(e)
                continue
