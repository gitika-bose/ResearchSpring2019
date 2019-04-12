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
        if(r[i, j] + g[i, j] + b[i, j] >= 475):
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



# from PIL import Image
# import PIL.ImageOps
# import pytesseract
# import argparse
# import cv2
# import os
# import imutils
# import numpy as np
#
# def sort_contours(cnts, method="left-to-right"):
#     # initialize the reverse flag and sort index
#     reverse = False
#     i = 0
#
#     # handle if we need to sort in reverse
#     if method == "right-to-left" or method == "bottom-to-top":
#         reverse = True
#
#     # handle if we are sorting against the y-coordinate rather than
#     # the x-coordinate of the bounding box
#     if method == "top-to-bottom" or method == "bottom-to-top":
#         i = 1
#
#     # construct the list of bounding boxes and sort them from top to
#     # bottom
#     boundingBoxes = [cv2.boundingRect(c) for c in cnts]
#     (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
#                                         key=lambda b: b[1][i], reverse=reverse))
#
#     # return the list of sorted contours and bounding boxes
#     return (cnts, boundingBoxes)
#
# def box_extraction(img_for_box_extraction_path, cropped_dir_path):
#     img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
#
#     # img_bin = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # (thresh, img_bin) = cv2.threshold(img, 128, 255,
#     #                                   cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
#     # img_bin = 255 - img_bin  # Invert the image
#     img_bin = img
#     cv2.imwrite("Image_bin.jpg", img_bin)
#
#     # Defining a kernel length
#     kernel_length = np.array(img).shape[1] // 40
#
#     # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
#     verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
#     # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
#     hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
#     # A kernel of (3 X 3) ones.
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     # Morphological operation to detect verticle lines from an image
#     img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
#     verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
#     cv2.imwrite("verticle_lines.jpg", verticle_lines_img)
#     # Morphological operation to detect horizontal lines from an image
#     img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
#     horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
#     cv2.imwrite("horizontal_lines.jpg", horizontal_lines_img)
#     # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
#     alpha = 0.5
#     beta = 1.0 - alpha
#     # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
#     img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
#     img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
#     (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#     # For Debugging
#     # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
#     cv2.imwrite("img_final_bin.jpg", img_final_bin)
#     cv2.imshow("Output", img_final_bin)
#     cv2.waitKey(0)
#
#     # Find contours for image, which will detect all the boxes
#     contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     # Sort all the contours by top to bottom.
#     (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
#     idx = 0
#     for c in contours:
#         # Returns the location and width,height for every contour
#         x, y, w, h = cv2.boundingRect(c)
#         # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
#         if (w > 80 and h > 20) and w > 3 * h:
#             idx += 1
#             new_img = img[y:y + h, x:x + w]
#             cv2.imwrite(cropped_dir_path + str(idx) + '.png', new_img)
#
# # def detect(c):
# #     # initialize the shape name and approximate the contour
# #     shape = "unidentified"
# #     peri = cv2.arcLength(c, True)
# #     approx = cv2.approxPolyDP(c, 0.01 * peri, True)
# #     # if the shape has 4 vertices, it is either a square or
# #     # a rectangle
# #     if len(approx) == 4:
# #         # compute the bounding box of the contour and use the
# #         # bounding box to compute the aspect ratio
# #         (x, y, w, h) = cv2.boundingRect(approx)
# #         ar = w / float(h)
# #
# #         # a square will have an aspect ratio that is approximately
# #         # equal to one, otherwise, the shape is a rectangle
# #         shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
# #
# #
# #     # return the name of the shape
# #     return shape
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
# # Convert non-black pixels to white
# for i in range(w):
#     for j in range(h):
#         # if(r[i, j] >= 100 or g[i, j] >= 100 or b[i, j] >= 100):
#         #     r[i, j] = 255 # Just change R channel
#         if(r[i, j] + g[i, j] + b[i, j] >= 475):
#             r[i, j] = 255 # Just change R channel
#         else:
#             r[i, j] = 0
#
# # Merge just the R channel as all channels
# im = Image.merge('RGB', (R, R, R))
#
# im.save("new.png")
#
# box_extraction("new.png", "./Cropped/")
#
#
# # gray = cv2.imread("new.png")
# #
# # gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
#
#
#
# # cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # cnts = imutils.grab_contours(cnts)
# #
# # for c in cnts:
# #     c = c.astype("float")
# #     # c *= ratio
# #     c = c.astype("int")
# #     shape = detect(c)
# #     cv2.drawContours(gray, [c], -1, (0, 255, 0), 2)
# #     print(shape)
# # cv2.imshow("Output", gray)
# # cv2.waitKey(0)
#
# # gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
# #             cv2.THRESH_BINARY,11,2)
#
#
#
#
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
# #
# # # # show the output images
# # cv2.imshow("Output", gray)
# # cv2.waitKey(0)