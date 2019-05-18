import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join


shapes = ['capsule', 'diamond', 'freeform', 'hexagon', 'octagon', 'oval', 'pentagon',
          'rectangle', 'round', 'semi-circle', 'square', 'tear', 'trapezoid', 'triangle']
root_folder = 'images/full/'

chars_b = [chr(l) for l in range(65,91)]
chars_s = [chr(l) for l in range(97,123)]
nums = [str(l) for l in range(0,10)]
sp = ['-',',','(',')',':','+','.','/']

letters = {l:0 for l in chars_b}
for l in nums: letters[l]=0
for l in chars_s: letters[l]=0
for l in sp: letters[l]=0

for shape in shapes:
    files = [root_folder+shape+'/annotations/'+f for f in listdir(root_folder+shape+'/annotations/') if (isfile(join(root_folder+shape+'/annotations/', f)) and '.xml' in f)]
    for file in files:
        tree = ET.parse(file)
        root = tree.getroot()
        check = set()
        for child in root:
            if child.tag == 'object':
                name = child[0].text.strip()
                # print(file)
                if name in check: check.remove(name)
                else:
                    letters[name] += 1
                    check.add(name)

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

file_write = open('all_letters_xml1.txt', 'w')
file_write.write(output)