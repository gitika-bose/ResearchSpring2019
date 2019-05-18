from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import random
from shutil import copyfile
import os

# # Checking
# root_folder = './dataset_numbers/'
# xml_folder = root_folder + 'xmls/'
# xml_files = [f for f in listdir(xml_folder) if (isfile(join(xml_folder, f)) and '.xml' in f)]
# numbers = [str(i) for i in range(0,10)]
# for n in numbers:
#     folder = root_folder + n + '/'
#     files = [f for f in listdir(folder) if (isfile(join(folder, f)) and '.png' in f)]
#     for f in files:
#         name = f.split('.')[0]
#         if name+'.xml' not in xml_files: print(n, name)

counts = {0:400, 1:400, 2:400, 5:400, 3:380, 4:345, 7:280, 9:250, 6:210, 8:200}

root_folder = './dataset_numbers/'
xml_folder = root_folder + 'xmls/'
images_folder = root_folder + 'images/'
numbers = [str(i) for i in range(0,10)]
# numbers = ['0']
main_csv = root_folder + 'dataset_numbers_csv.csv'
main_output = ''
for n in numbers:
    folder = root_folder + n + '/'
    csv_file = folder + 'dataset_' + n + '_csv.csv'
    files = list(set([f for f in listdir(folder) if (isfile(join(folder, f)) and '.png' in f)]))
    # for f in files: copyfile(folder+f,images_folder+f)
    output = ''

    train = random.sample(files,counts[int(n)])
    for t in train: files.remove(t)
    validate = random.sample(files, counts[int(n)]//10)
    for v in validate: files.remove(v)
    train_count,validate_count,test_count = 0,0,0
    for f in train:
        name = f.split('.')[0]
        xml_file = xml_folder + name + '.xml'

        tree = ET.parse(xml_file)
        root = tree.getroot()

        filename = root[1].text
        org_dim = root[2]
        width, height = int(org_dim[0].text), int(org_dim[1].text)
        check = False
        for child in root:
            if child.tag == 'object':
                name = child[0].text
                if str(name) == n:
                    xmin, ymin = int(child[5][0].text) / width, int(child[5][1].text) / height
                    xmax, ymax = int(child[5][2].text) / width, int(child[5][3].text) / height
                    if check:
                        output += 'TEST,gs://' + folder + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                                  + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        main_output += 'TEST,gs://research-pill/dataset_numbers/images/' + filename + ',' + n + ',' + str(
                            xmin) + ',' + str(ymin) \
                                       + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        test_count += 1
                    else:
                        output += 'TRAIN,gs://' + folder + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                                + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        main_output += 'TRAIN,gs://research-pill/dataset_numbers/images/' + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                                  + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        check = True
                        train_count += 1

    for f in validate:
        name = f.split('.')[0]
        xml_file = xml_folder + name + '.xml'

        tree = ET.parse(xml_file)
        root = tree.getroot()

        filename = root[1].text
        org_dim = root[2]
        width, height = int(org_dim[0].text), int(org_dim[1].text)
        check = False
        for child in root:
            if child.tag == 'object':
                name = child[0].text
                if str(name) == n:
                    xmin, ymin = int(child[5][0].text) / width, int(child[5][1].text) / height
                    xmax, ymax = int(child[5][2].text) / width, int(child[5][3].text) / height
                    if check:
                        output += 'TEST,gs://' + folder + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                                  + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        main_output += 'TEST,gs://research-pill/dataset_numbers/images/' + filename + ',' + n + ',' + str(
                            xmin) + ',' + str(ymin) \
                                       + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        test_count += 1
                    else:
                        output += 'VALIDATE,gs://' + folder + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                                + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        main_output += 'VALIDATE,gs://research-pill/dataset_numbers/images/' + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                                  + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        check = True
                        validate_count += 1

    for f in files:
        name = f.split('.')[0]
        xml_file = xml_folder + name + '.xml'

        tree = ET.parse(xml_file)
        root = tree.getroot()

        filename = root[1].text
        org_dim = root[2]
        width, height = int(org_dim[0].text), int(org_dim[1].text)
        for child in root:
            if child.tag == 'object':
                name = child[0].text
                if str(name) == n:
                    xmin, ymin = int(child[5][0].text) / width, int(child[5][1].text) / height
                    xmax, ymax = int(child[5][2].text) / width, int(child[5][3].text) / height
                    output += 'TEST,gs://' + folder + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                            + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                    main_output += 'TEST,gs://research-pill/dataset_numbers/images/' + filename + ',' + n + ',' + str(xmin) + ',' + str(ymin) \
                              + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                    test_count += 1

    file = open(csv_file, 'w')
    file.write(output)
    print(train_count,validate_count,test_count)
file = open(main_csv, 'w')
file.write(main_output)