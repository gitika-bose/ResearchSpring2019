### Directories:
* post_images: Images post processing

### Files(Code):
To run any file type: python <file_name.py> <imagepath>

* color: Small List of Color and their rgb
* color2: Large List of Color and their rgb
* extract_shape_color:
    * python extract_shape_color.py <imagepath>
    * Extracts shape and color
    * Shape: through contour detection and approxPolyDP
    * Color: through contour detection and euclidean distance
* extract_blue: 
    * Extract color blue if it is present