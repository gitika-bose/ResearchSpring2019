import os
import subprocess
import shutil

shapes = ['bullet', 'capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

trials = ['trial'+str(x+1) for x in range(5)]
# trials = ['trial3']
main_folder = 'pill_shapes/'
temp_folder = 'templates/'
type = 'front'
compare_folder = main_folder + 'compare/'
if os.path.isdir(compare_folder):
    shutil.rmtree(compare_folder)
os.mkdir(compare_folder)

for shape in trials:
# for shape in shapes:
# shape = 'round'
    folder = main_folder + shape + "/"
    compare = folder+shape+'-compare/'
    if os.path.isdir(compare):
        shutil.rmtree(compare)
    os.mkdir(compare)
    open(folder+shape+'-compare.txt', 'w').close()
    open(compare_folder+shape+'-compare.txt', 'w').close()
    subprocess.check_output(['python', 'grabcut_02.py', shape, type])

    for template in shapes:
        subprocess.check_output(['python','compare_image_template.py',shape,template])

