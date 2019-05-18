import json
import sys

file_name = 'data.json'
file = open(file_name,'r')
data = json.load(file)

shapes = {}
for shape in data:
    if shape not in shapes: shapes[shape] = set()
    for name in data[shape]['data']: shapes[shape].add(name)

write_file = open('shapes.json','w')
imprints_list = {k:sorted(list(v)) for k,v in shapes.items()}
json.dump(imprints_list, write_file, indent=2)

# shape_data = data[shape]['data'][name]
# print(json.dumps(shape_data, indent=2))
