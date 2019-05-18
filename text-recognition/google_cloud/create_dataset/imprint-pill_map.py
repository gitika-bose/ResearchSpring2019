import json
import sys

file_name = 'data.json'
file = open(file_name,'r')
data = json.load(file)

imprints = {}
for shape in data:
    for name,shape_data in data[shape]['data'].items():
        imprint = shape_data.get('imprint_list',None)
        if not imprint: imprint = [shape_data.get('imprint',None)]
        if not imprint or imprint == [None]: continue
        for word in imprint:
            for w in word:
                if w not in imprints: imprints[w] = set()
                imprints[w].add(name)

write_file = open('imprints.json','w')
imprints_list = {k:list(v) for k,v in imprints.items()}
json.dump(imprints_list, write_file, indent=2)

# shape_data = data[shape]['data'][name]
# print(json.dumps(shape_data, indent=2))
