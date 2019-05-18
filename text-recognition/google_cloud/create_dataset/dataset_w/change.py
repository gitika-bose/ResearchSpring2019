# import csv
# file = csv.reader(open('dataset_w.csv'), delimiter=',')
# writer_f = csv.writer(open('dataset_w2.csv','w'), delimiter=',')
# count = 0
# for h in file:
#     d = h
#     if count > 45: d[0]='TEST'
#     elif 40 < count <= 45: d[0]='VALIDATE'
#     else: d[0]='TRAIN'
#     writer_f.writerow(d)
#     count +=1

import csv
from os import listdir
from os.path import isfile, join
folder_t, folder_v = './dataset', './dataset_v'
files_t = [f for f in listdir(folder_t) if (isfile(join(folder_t, f)) and '.png' in f)]
files_v = [f for f in listdir(folder_v) if (isfile(join(folder_v, f)) and '.png' in f)]
file = csv.reader(open('dataset_w.csv'), delimiter=',')
writer_f = csv.writer(open('dataset_w3.csv','w'), delimiter=',')
for h in file:
    name = h[1].split('/')[-1]
    d = h
    if name in files_t:
        d[0] = 'TRAIN'
    elif name in files_v:
        d[0] = 'VALIDATE'
    else:
        d[0]='TEST'
    writer_f.writerow(d)



