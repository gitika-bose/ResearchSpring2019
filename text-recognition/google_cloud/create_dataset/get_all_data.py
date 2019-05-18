import requests
import json

def next_count(count):
    count = int(count)
    count+=1
    if count < 10: return '000'+str(count)
    elif count <100: return '00'+str(count)
    elif count <1000: return '0'+str(count)
    else: return str(count)

def only_alpha(name):
    start, end = 0, 0
    for i in range(len(name)):
        word=name[i]
        if str(word).isalpha():
            start=i
            break
    for i in range(len(name)-1,-1,-1):
        word=name[i]
        if str(word).isalpha():
            end=i
            break
    name = name[start:end+1]
    name.strip()
    return name

def format_name(name):
    name_split = None
    if '/' in name:
        name_split = []
        if 'Pack' in name or 'pack' in name or 'PACK' in name:
            name = name[:-4]
            name.strip()
            name_split = [only_alpha(n) for n in name.split('/')]
    return name_split

file = open('data.json', 'w')
shapes = ['bullet','capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
base_url = 'https://rximage.nlm.nih.gov/api/rximage/1/rxnav?rLimit=4000&includeMpc=true&shape='
data = {}
for shape in shapes:
    count = '0001'
    r = requests.get(base_url+shape).json()
    data[shape] = {}
    data[shape]['data']={}
    for entry in r['nlmRxImages']:
        key = count+shape
        data[shape]['data'][key] = entry['mpc']
        data[shape]['data'][key]['name'] = entry['name']
        data[shape]['data'][key]['id'] = entry['id']
        data[shape]['data'][key]['imageUrl'] = entry['imageUrl']

        color_list = None
        if ',' in entry['mpc']['color']: color_list = [e.strip() for e in entry['mpc']['color'].split(',')]
        data[shape]['data'][key]['color_list'] = color_list

        name_list = format_name(entry['name'])
        data[shape]['data'][key]['name_list'] = name_list

        if 'imprint' in entry['mpc']:
            imprint_list = None
            if';' in entry['mpc']['imprint']: imprint_list = [e.strip() for e in entry['mpc']['imprint'].split(';')]
            data[shape]['data'][key]['imprint_list'] = imprint_list

        count = next_count(count)
    data[shape]['info']={
        'total_number':count
    }

json.dump(data, file, indent=2)
