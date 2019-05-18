import urllib.request
from PIL import Image
import json


shapes = ['bullet','capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

file_name = 'data.json'
file = open(file_name, 'r')
data = json.load(file)

folder1 = 'images/full/'

for shape in shapes:
    shape_data = data[shape]['data']
    print('\nDownloading', shape)
    for name in shape_data:
        try:
            file1 = folder1 + shape + '/' + name + '.png'
            temp_file_name = 'trial.jpg'
            url = shape_data[name]['imageUrl']
            urllib.request.urlretrieve(url, temp_file_name)

            img = Image.open(temp_file_name)
            width, height = img.size
            remove = (50, 0, width, height-180)
            new_img = img.crop(remove)
            new_img.save(file1, 'PNG')
        except Exception as e:
            print('Exception: ', e, name)
            continue
    print('Downloaded',data[shape]['info']['total_number'])

# img2 = Image.open('new_image.png')
# width2, height2 = img2.size
# remove2 = (0, 0, width2, height2/2)
# new_img2 = new_img.crop(remove2)
# new_img2.save('new_image2.png', 'PNG')