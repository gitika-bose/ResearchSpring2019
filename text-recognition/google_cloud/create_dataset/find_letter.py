import json
import sys

shapes = ['capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

file_name = 'data.json'
file = open(file_name, 'r')
data = json.load(file)

letter = sys.argv[1]
write_file = open(letter+'.txt','w')

let = []
for shape in shapes:
    shape_data = data[shape]['data']
    for name in shape_data:
        imprint = shape_data[name].get('imprint',None)
        if imprint:
            if letter in imprint:
                let.append(name)
                write_file.write(name+'\n')
print(let)
