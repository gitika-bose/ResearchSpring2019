import json
import sys

file_name = 'data.json'
file = open(file_name,'r')
data = json.load(file)

colors = {}
for shape in data:
    for name,shape_data in data[shape]['data'].items():
        color = shape_data.get('color_list', None)
        if not color: color = [shape_data.get('color', None)]
        if not color or color == [None]: continue

        for c in color:
            if c.lower() not in colors: colors[c.lower()] = set()
            colors[c.lower()].add(name)

write_file = open('colors.json','w')
imprints_list = {k:list(v) for k,v in colors.items()}
json.dump(imprints_list, write_file, indent=2)

# shape_data = data[shape]['data'][name]
# print(json.dumps(shape_data, indent=2))
