import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

folder2 = 'w_s/annotations/'
files = [folder2+f for f in listdir(folder2) if isfile(join(folder2, f))]
output = ''

folder = 'dataset_w/'
file_name = folder + 'dataset_w.csv'

for file in files:
    tree = ET.parse(file)
    root = tree.getroot()

    filename = root[1].text
    org_dim = root[2]
    width, height = int(org_dim[0].text), int(org_dim[1].text)
    for child in root:
        if child.tag == 'object':
            name = child[0].text
            xmin, ymin = int(child[5][0].text)/width, int(child[5][1].text)/height
            xmax, ymax = int(child[5][2].text)/width, int(child[5][3].text)/height
            output += 'UNASSIGNED,gs://research-pill/' + folder + filename + ',' + name + ',' + str(xmin) + ',' + str(ymin) \
                      + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
file = open(file_name, 'w')
file.write(output)