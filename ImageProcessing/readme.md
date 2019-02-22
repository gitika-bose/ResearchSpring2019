###Directories:
* other_images: Random Images
* pill_images: Images of pills 

###Files(Code):
To run any file type: python <file_name.py> <imagepath>

* run_all: Runs:
    * edge_detect
    * extract_background_own
    * extract_background_own_02
    * extract_shape_color
    * grabcut
* canny_edge: 
    * Canny Edge detection 
    * Slider to check which threshold works best 
* color: Small List of Color and their rgb
* color2: Large List of Color and their rgb
* edge_detect: 
    * Detect edge using a weird algo (working on understanding it currently)
* extract_background_own:
    * Finds the mean of a template chosen by us (say 25 * 25 pixels) and check which pixel in the image is within mean and std.
* extract_background_own_02:
    * Records different colors within the template chosen by us (say 25 * 25 pixels) and check which pixel in the image is within the list of colors
* extract_shape_color:
    * Extracts shape and color
    * Shape: through contour detection and approxPolyDP
    * Color: through contour detection and euclidean distance
* extract_blue: 
    * Extract color blue if it is present
* grabcut:
    * Common cv2 Algorithm to extract foreground
    * User inputs where foreground is located
* Image_types:
    * Shows different types of thresholded images, for comparison

