import requests

def write(l,filename):
    line = ""
    for a in l:
        line += a[0] + ": " + str(a[1]) + "\n"
    open(filename,'w').write(line)

colors = ['BLACK', 'BLUE', 'BROWN', 'GRAY', 'GREEN', 'ORANGE', 'PINK', 'PURPLE', 'RED', 'TURQUOISE', 'WHITE', 'YELLOW']
shapes = ['bullet', 'capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

base_url = 'https://rximage.nlm.nih.gov/api/rximage/1/rxnav?rLimit=1'
color_url = base_url+'&color='
shape_url = base_url+'&shape='
color_list, shape_list, shape_color_list = [], [], []

for color in colors:
    r = requests.get(color_url+color).json()
    color_list.append([color, r['replyStatus']['totalImageCount']])
color_list.sort(key=lambda x:x[1], reverse=True)
write(color_list,'top_colors.txt')

for shape in shapes:
    r = requests.get(shape_url+shape).json()
    shape_list.append([shape, r['replyStatus']['totalImageCount']])
shape_list.sort(key=lambda x:x[1], reverse=True)
write(shape_list,'top_shapes.txt')

for color in colors:
    for shape in shapes:
        shape_color = shape+'-'+color
        color_shape_url = base_url + '&color=' + color + '&shape=' + shape
        r = requests.get(color_shape_url).json()
        shape_color_list.append([shape_color, r['replyStatus']['totalImageCount']])
shape_color_list.sort(key=lambda x:x[1], reverse=True)
write(shape_color_list,'top_shape_color.txt')



