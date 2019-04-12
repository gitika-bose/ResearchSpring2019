import cv2
import numpy as np


img = cv2.imread('pill_shapes/capsule2/capsule2-front_grabcut.jpg')
cv2.imshow("Original image",img)

# img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
# cv2.imshow(" image",img)
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=50., tileGridSize=(8,8))

lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
l, a, b = cv2.split(lab)  # split on 3 different channels

l2 = clahe.apply(l)  # apply CLAHE to the L-channel

lab = cv2.merge((l2,a,b))  # merge channels
img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
cv2.imshow('Increased contrast', img2)







dst = cv2.fastNlMeansDenoisingColored(img2,None,30,30,7,21)
cv2.imshow(' contrast', dst)


# cv2.imwrite('sunset_modified.jpg', img2)

def display(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)


def LAB_delta(delta, img):
    h, w = img.shape[:2]
    for i in range(h):
        for j in range(w):
            img[i][j][0] += delta
    # return img


img = img2.copy()
# img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
# LAB_delta(80,img)

height, width = img.shape[:2]
mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (5, 5, img.shape[1] - 5, img.shape[0] - 5)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask2[:, :, np.newaxis]






Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 2
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

cv2.imshow('res2',res2)
cv2.imwrite('trial_5.jpg', res2)
cv2.waitKey(0)
cv2.destroyAllWindows()










# import numpy as np
# import cv2
#
# img = cv2.imread('pill_shapes/trial2/trial2_front.jpg')
# Z = img.reshape((-1,3))
#
# # convert to np.float32
# Z = np.float32(Z)
#
# # define criteria, number of clusters(K) and apply kmeans()
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
# K = 5
# ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
# print(ret,label,center)
# # Now convert back into uint8, and make original image
# center = np.uint8(center)
# res = center[label.flatten()]
# res2 = res.reshape((img.shape))
#
# cv2.imshow('res2',res2)
# cv2.imwrite('trial_5.jpg', res2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()














# from PIL import Image
# import PIL.ImageOps
# import pytesseract
# import argparse
# import cv2
# import os
# import numpy as np
#
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#                 help="path to input image to be OCR'd")
# ap.add_argument("-p", "--preprocess", type=str, default="thresh",
#                 help="type of preprocessing to be done")
# args = vars(ap.parse_args())
#
# # load the example image and convert it to grayscale
# # print(args["image"])
#
# filename = args["image"]
# im_orig = cv2.imread(filename)
#
# im_lab = cv2.cvtColor(im_orig, cv2.COLOR_BGR2LAB)
#
# im_orig = cv2.cvtColor(im_orig, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Image", im_orig)
# # im_orig = cv2.imread(filename,1)
#
# im = Image.open(filename)
# R, G, B = im.convert('RGB').split()
# r = R.load()
# g = G.load()
# b = B.load()
# w, h = im.size
#
#
# # Convert non-black pixels to white
# for i in range(w):
#     for j in range(h):
#         # if(r[i, j] >= 100 or g[i, j] >= 100 or b[i, j] >= 100):
#         #     r[i, j] = 255 # Just change R channel
#
#         print("\n", im_lab[i][j])
#
#         if(r[i, j] + g[i, j] + b[i, j] >= 505):
#             r[i, j] = 255 # Just change R channel
#         elif(r[i, j] + g[i, j] + b[i, j] >= 490):
#             r[i, j] = 105
#         else:
#             r[i, j] = 0
#
# # Merge just the R channel as all channels
# im = Image.merge('RGB', (R, R, R))
#
# im.save("new.png")
#
#
# #
# #
# # image = cv2.imread("new.png")
# #
# # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #
# # # gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
# # #             cv2.THRESH_BINARY,11,2)
# #
# # file2 = "{}.png".format(os.getpid())
# # cv2.imwrite(file2, gray)
# #
# #
# # config = ('--tessdata-dir "./" -l eng --oem 1 psm 3')
# # text = pytesseract.image_to_string(Image.open(file2),config=config)
# # # text = pytesseract.image_to_string(gray, config=config)
# # os.remove(file2)
# # os.remove("new.png")
# # print(text)
#
# # # show the output images
# # cv2.imshow("Output", gray)
# # cv2.waitKey(0)