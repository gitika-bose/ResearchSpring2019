from PIL import Image
import PIL.ImageOps
import pytesseract
import argparse
import cv2
import os
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
# print(args["image"])

filename = args["image"]
im_orig = cv2.imread(filename)
im_orig = cv2.cvtColor(im_orig, cv2.COLOR_BGR2GRAY)
cv2.imshow("Image", im_orig)
# im_orig = cv2.imread(filename,1)

im = Image.open(filename)
R, G, B = im.convert('RGB').split()
r = R.load()
g = G.load()
b = B.load()
w, h = im.size

# Convert non-black pixels to white
for i in range(w):
    for j in range(h):
        # if(r[i, j] >= 100 or g[i, j] >= 100 or b[i, j] >= 100):
        #     r[i, j] = 255 # Just change R channel
        if(r[i, j] + g[i, j] + b[i, j] >= 479):
            r[i, j] = 255 # Just change R channel
        else:
            r[i, j] = 0

# Merge just the R channel as all channels
im = Image.merge('RGB', (R, R, R))

im.save("new.png")




image = cv2.imread("new.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY,11,2)

file2 = "{}.png".format(os.getpid())
cv2.imwrite(file2, gray)


config = ('--tessdata-dir "./" -l eng --oem 1 psm 3')
text = pytesseract.image_to_string(Image.open(file2),config=config)
# text = pytesseract.image_to_string(gray, config=config)
os.remove(file2)
os.remove("new.png")
print(text)

# # show the output images
cv2.imshow("Output", gray)
cv2.waitKey(0)