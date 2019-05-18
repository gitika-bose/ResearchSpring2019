from os import listdir
from os.path import isfile, join, isdir
import xml.etree.ElementTree as ET
import random
from shutil import copyfile
import os

# # Checking
# root_folder = './dataset_letters/'
# xml_folder = root_folder + 'xmls/'
# xml_files = [f for f in listdir(xml_folder) if (isfile(join(xml_folder, f)) and '.xml' in f)]
# letters = [f for f in listdir(root_folder) if (isdir(join(root_folder, f)) and f not in ['xmls','images'])]
# for l in letters:
#     folder = root_folder + l + '/'
#     train = [f for f in listdir(folder + 'train/') if (isfile(join(folder + 'train/', f)) and '.png' in f)]
#     validate = [f for f in listdir(folder + 'validate/') if (isfile(join(folder + 'validate/', f)) and '.png' in f)]
#     test = [f for f in listdir(folder + 'test/') if (isfile(join(folder + 'test/', f)) and '.png' in f)]
#     print(l)
#     for f in train:
#         name = f.split('.')[0]
#         if name+'.xml' not in xml_files: print(l, 'train', name)
#     for f in test:
#         name = f.split('.')[0]
#         if name+'.xml' not in xml_files: print(l, 'test', name)
#     for f in validate:
#         name = f.split('.')[0]
#         if name+'.xml' not in xml_files: print(l, 'validate', name)


root_folder = './dataset_letters/'
xml_folder = root_folder + 'xmls/'
images_folder = root_folder + 'images/'
letters = [f for f in listdir(root_folder) if (isdir(join(root_folder, f)) and f not in ['xmls','images'])]
# numbers = ['0']
main_csv = root_folder + 'dataset_letters_csv.csv'
main_output = ''
for l in letters:
    letter = l if len(l) == 1 else l[0]
    folder = root_folder + l + '/'
    csv_file = folder + 'dataset_' + l + '_csv.csv'

    images = folder + 'images/'
    os.mkdir(images)
    # files = list(set([f for f in listdir(folder) if (isfile(join(folder, f)) and '.png' in f)]))
    # for f in files: copyfile(folder+f,images_folder+f)
    output = ''
    count = 0

    train = list(set([f for f in listdir(folder + 'train/') if (isfile(join(folder + 'train/', f)) and '.png' in f)]))
    validate = list(set([f for f in listdir(folder + 'validate/') if (isfile(join(folder + 'validate/', f)) and '.png' in f)]))
    test = list(set([f for f in listdir(folder + 'test/') if (isfile(join(folder + 'test/', f)) and '.png' in f)]))
    # for f in train: copyfile(folder + 'train/' + f, images_folder + f)
    # for f in test: copyfile(folder + 'test/' + f, images_folder + f)
    # for f in validate: copyfile(folder + 'validate/' + f, images_folder + f)
    for f in train:
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
                if str(name) == letter:
                    xmin, ymin = int(child[5][0].text) / width, int(child[5][1].text) / height
                    xmax, ymax = int(child[5][2].text) / width, int(child[5][3].text) / height
                    output += 'UNASSIGNED,gs://' + folder + filename + ',' + letter + ',' + str(xmin) + ',' + str(ymin) \
                              + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                    main_output += 'UNASSIGNED,gs://research-pill/dataset_letters/images/' + filename + ',' + letter + ',' + str(
                        xmin) + ',' + str(ymin) \
                                   + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                    count += 1
        copyfile(folder + 'train/' + f, images + f)
        copyfile(folder + 'train/' + f, images_folder + f)
        if count >=100: break

    if count <100:
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
                    if str(name) == letter:
                        xmin, ymin = int(child[5][0].text) / width, int(child[5][1].text) / height
                        xmax, ymax = int(child[5][2].text) / width, int(child[5][3].text) / height
                        output += 'UNASSIGNED,gs://' + folder + filename + ',' + letter + ',' + str(xmin) + ',' + str(ymin) \
                                  + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        main_output += 'UNASSIGNED,gs://research-pill/dataset_letters/images/' + filename + ',' + letter + ',' + str(
                            xmin) + ',' + str(ymin) \
                                       + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        count += 1
            copyfile(folder + 'validate/' + f, images + f)
            copyfile(folder + 'validate/' + f, images_folder + f)
            if count >= 100: break

    if count < 100:
        for f in test:
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
                    if str(name) == letter:
                        xmin, ymin = int(child[5][0].text) / width, int(child[5][1].text) / height
                        xmax, ymax = int(child[5][2].text) / width, int(child[5][3].text) / height
                        output += 'UNASSIGNED,gs://' + folder + filename + ',' + letter + ',' + str(xmin) + ',' + str(ymin) \
                                + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        main_output += 'UNASSIGNED,gs://research-pill/dataset_letters/images/' + filename + ',' + letter + ',' + str(xmin) + ',' + str(ymin) \
                                  + ',,,' + str(xmax) + ',' + str(ymax) + ',,\n'
                        count += 1
            copyfile(folder + 'test/' + f, images + f)
            copyfile(folder + 'test/' + f, images_folder + f)
            if count >=100: break

    file = open(csv_file, 'w')
    file.write(output)
    print(letter, count)
file = open(main_csv, 'w')
file.write(main_output)
