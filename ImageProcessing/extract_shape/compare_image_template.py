import cv2
import numpy as np
import sys
import imutils


def display(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

shape = sys.argv[1] # semi-circle
template_name = sys.argv [2]

imagepath = '../images/pill_shapes/' + shape + '/' + shape + '-front_extract.jpg'
templatepath = '../images/templates/' + template_name + '.png'

compare_txt = '../images/pill_shapes/' + shape + '/' + shape + "-compare.txt"
compare = '../images/pill_shapes/' + shape + '/' + shape + "-compare/"
# print(img_shape,temp_shape)
compare_str = shape + '-' + template_name
file = compare + compare_str + ".jpg"
img = cv2.imread(imagepath)
# display("Image",img)

img = imutils.resize(img, width=300)
h_i,w_i = img.shape[:2]
template = cv2.imread(templatepath)
template = imutils.resize(template, width=300)
# display("Template",template)
h_t,w_t = template.shape[:2]
for i in range(h_t):
    for j in range(w_t):
        if template[i][j][0] == 0 and template[i][j][1] == 0 and template[i][j][2] == 0:
            template[i][j][0],template[i][j][1],template[i][j][2] = 255,255,255
        elif template[i][j][0] == 255 and template[i][j][1] == 255 and template[i][j][2] == 255:
            continue
        else:
            template[i][j][0],template[i][j][1],template[i][j][2] = 0,0,0

# display("Original",img)
# display("Template", template)
if h_i >= h_t*2 or h_t >= h_i*2:
    line = compare_str + ': Can\'t compare\n'
else:
    w = w_i if w_i < w_t else w_t
    h = h_i if h_i < h_t else h_t
    final = img[:h,:w] - template[:h,:w]
    cv2.imwrite(file, final)
    # display("Final",final)
    whites = np.sum(final == 255)

    line = compare_str + ': ' + str(whites) + '\n'
open(compare_txt,'a').write(line)
open('../images/pill_shapes/compare/'+ shape + "-compare.txt",'a').write(line)



