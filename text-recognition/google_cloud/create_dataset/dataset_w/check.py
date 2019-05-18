from os import listdir
from os.path import isfile, join
import cv2
from shutil import copyfile

folder = './'
files = [f for f in listdir(folder) if (isfile(join(folder, f)))]
yes, no = [], []
yes_folder, no_folder = 'train_validate/', 'test/'
for f in files:
    if '.png' in f:
        img = cv2.imread(f)
        cv2.imshow('Image',img)
        while (1):
            k = cv2.waitKey(1) & 0xFF
            if k == 121 or k == 89:
                cv2.imwrite(yes_folder + f,img)
                yes.append(f)
                print('Train/Validate:',f)
                break
            elif k == 110 or k == 78:
                cv2.imwrite(no_folder + f, img)
                no.append(f)
                print('Test:',f)
                break
