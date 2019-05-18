from os import listdir
from os.path import isfile, join, isdir
import os

images = ['0013oval','0042round','0043round','0044round','0047round','0061round','0066round','0069round',
          '0157oval','0271round','0272round','0461oval','0251oval','0254oval','1266round','0053round','0137oval',
          '0309oval','1283oval','1833round','0309oval','0054round','0069round','0157oval','0137oval','0218capsule',
          '0202oval','1833round','0309oval','0054round','0218capsule','0320oval','0202oval','0054round','1326oval', '0461oval',
          '0157oval', '1833round', '0272round', '0271round', '0137oval', '0309oval', '0157oval']

folder1, folder2 = './dataset_letters/', './dataset_numbers/'
folder1_folders = [f for f in listdir(folder1) if isdir(join(folder1, f))]
folder2_folders = [f for f in listdir(folder2) if isdir(join(folder2, f))]

count = 0
for sub_folder in folder1_folders:
    if sub_folder=='git' or sub_folder == 'xmls' or sub_folder == 'images': continue
    sub = folder1+sub_folder+'/'
    files = [f for f in listdir(sub) if (isfile(join(sub, f)) and '.png' in f)]
    for i in images:
        if i+'.png' in files:
            os.remove(sub+i+'.png')
            count += 1
    files = [f for f in listdir(sub+'test/') if (isfile(join(sub+'test/', f)) and '.png' in f)]
    for i in images:
        if i + '.png' in files:
            os.remove(sub +'test/'+ i + '.png')
            count += 1
    files = [f for f in listdir(sub + 'train/') if (isfile(join(sub + 'train/', f)) and '.png' in f)]
    for i in images:
        if i + '.png' in files:
            os.remove(sub + 'train/' + i + '.png')
            count += 1
    files = [f for f in listdir(sub + 'validate/') if (isfile(join(sub + 'validate/', f)) and '.png' in f)]
    for i in images:
        if i + '.png' in files:
            os.remove(sub + 'validate/' + i + '.png')
            count += 1

for sub_folder in folder2_folders:
    sub = folder2+sub_folder+'/'
    files = [f for f in listdir(sub) if (isfile(join(sub, f)) and '.png' in f)]
    for i in images:
        if i+'.png' in files:
            os.remove(sub+i+'.png')
            count += 1

print(count)
