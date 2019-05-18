import csv

file = open('./fda_data/Products.txt','r')
csv_file = csv.reader(file,delimiter='\t')
drugnames = set()
drugtypes = {}
check = True
output = ''
for line in csv_file:
    if check:
        check = False
    name = line[5].lower()
    type = line[2].lower()
    if name not in drugnames:
        output += name + '\n'
        drugnames.add(name)
        drugtypes[name] = type
open('drugs.txt','w').write(output)
# print(drugnames)
# print(len(drugnames))
