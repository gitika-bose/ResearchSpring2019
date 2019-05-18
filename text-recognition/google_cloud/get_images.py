shapes = ['capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
folder_dir = '../../ImageProcessing/images/pill_shapes/'
import subprocess
for shape in shapes:
    front = folder_dir + shape + '/' + shape + '_front.jpg'
    back = folder_dir + shape + '/' + shape + '_back.jpg'
    subprocess.check_output(['cp', front, './dataset01_images'])
    subprocess.check_output(['cp', back, './dataset01_images'])
