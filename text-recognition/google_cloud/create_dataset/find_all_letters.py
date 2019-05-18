import json
from PIL import Image

shapes = ['bullet','capsule', 'diamond', 'double_circle', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']

file_name = 'data.json'
file = open(file_name, 'r')
data = json.load(file)

chars_b = [chr(l) for l in range(65,91)]
chars_s = [chr(l) for l in range(97,123)]
nums = [str(l) for l in range(0,10)]
sp = ['-',',','(',')',':','+','.','/']

letters = {l:0 for l in chars_b}
for l in nums: letters[l]=0
for l in chars_s: letters[l]=0
for l in sp: letters[l]=0

for shape in shapes:
    print('Checking shape',shape)
    shape_data = data[shape]['data']
    for name in shape_data:
        try:
            imprint = shape_data[name].get('imprint_list',None)
            if imprint: imprint = ''.join(imprint)
            else: imprint = shape_data[name].get('imprint',None)
            if imprint:
                for i in list(imprint):
                    letters[i] += 1
        except Exception as e:
            print('Exception:',e,name)

# file_write = open('all_letters.json', 'w')
# json.dump(letters, file_write, indent=2)

output = ''
chars_b_count = [(l,letters[l]) for l in letters if l in chars_b]
chars_s_count = [(l,letters[l]) for l in letters if l in chars_s]
nums_count = [(l,letters[l]) for l in letters if l in nums]
sp_count = [(l,letters[l]) for l in letters if l in sp]

chars_b_count.sort(key=lambda x:x[1], reverse=True)
chars_s_count.sort(key=lambda x:x[1], reverse=True)
nums_count.sort(key=lambda x:x[1], reverse=True)
sp_count.sort(key=lambda x:x[1], reverse=True)

for a in chars_b_count: output += str(a[0]) + ':' + str(a[1]) + '\n'
output += '\n'
for a in chars_s_count: output += str(a[0]) + ':' + str(a[1]) + '\n'
output += '\n'
for a in nums_count: output += str(a[0]) + ':' + str(a[1]) + '\n'
output += '\n'
for a in sp_count: output += str(a[0]) + ':' + str(a[1]) + '\n'

file_write = open('all_letters.txt', 'w')
file_write.write(output)