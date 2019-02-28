### Directories:
* post_images: Images post processing

### Files(Code):

#### Auto-Run Files:
* compare_image_template_all:
    * Runs grabcut_02.py and then compare_image_template.py on given images.
    * Shape images located in ../images/pill_shapes/
    * Template shapes located in ../images/templates/
* delete.py:
    * Deletes all Compare folders in each shape in ../images/pill_shapes/
* run_all: 
    * Auto-run file, update file names in the file
    * Runs:
        * edge_detect
        * extract_background_own
        * extract_background_own_02
        * grabcut
    
#### Others
* canny_edge_slide:
    * python canny_edge_slide.py <imagepath> 
    * Canny Edge detection with Slider to check which threshold works best 
* compare_image_template:
    * python compare_image_template.py <shape_name> <template_name>
    * shape_name - image of extracted contour located in ../images/pill_shapes/<shape>/<shape>-front_extract.jpg
    * template_name - template of shape to be compared located in ../images/pill_shapes/<template_name>.jpg
    * Compares the Image Shape extracted from an extraction algorithm to a template of given shape
* edge_detect: 
    * python edge_detect.py <imagepath>
    * Detect edge using a weird algo
    * https://www.codepasta.com/computer-vision/2016/11/06/background-segmentation-removal-with-opencv.html
* extract_background_own:
    * python extract_background_own.py <imagepath>
    * Finds the mean of a template chosen by us (say 25 * 25 pixels) 
        and check which pixel in the image is within mean and std.
* extract_background_own_02:
    * python extract_background_own_02.py <imagepath>
    * Records different colors within the template chosen by us (say 25 * 25 pixels) 
        and check which pixel in the image is within the list of colors
* grabcut:
    * python grabcut.py <imagepath>
    * Common cv2 Algorithm to extract foreground
* grabcut_02:
    * python grabcut_02.py <shape_name> <type>
    * shape - image of extracted contour located in ../images/pill_shapes/<shape>/<shape>-<type>.jpg
    * type - type of image to be taken from the folder - front or back (Shown with shape_name query)
    * Runs grabcut and then extracts contour and draws it on a new image, 
        saving it as ../images/pill_shapes/<shape>/<shape>-front_extract.jpg
* Image_types:
    * Shows different types of thresholded images, for comparison
    * python Image_types.py <imagepath>

