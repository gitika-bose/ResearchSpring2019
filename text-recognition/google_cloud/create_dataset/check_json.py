import json
import sys

file_name = '/Users/tejitpabari/Desktop/ResearchSpring2019/text-recognition/google_cloud/create_dataset/data.json'
file = open(file_name,'r')
data = json.load(file)

name = sys.argv[1]
shape = name[4:]
shape_data = data[shape]['data'][name]
print(json.dumps(shape_data, indent=2))
