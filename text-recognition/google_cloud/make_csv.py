folder = './dataset01_images/'
file_name = folder + 'dataset01.csv'
shapes = ['capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
output = ''
for shape in shapes:
    front = 'UNASSIGNED,gs://research-pill/dataset01_images/' + shape + '_front.jpg,,,,,,,,,\n'
    back = 'UNASSIGNED,gs://research-pill/dataset01_images/' + shape + '_back.jpg,,,,,,,,,\n'
    output += front + back
file = open(file_name, 'w')
file.write(output)