import subprocess
import sys
import cv2
# canny_edge = 'canny_edge.py'
edge_detect = 'edge_detect.py'
extract_background_own = 'extract_background_own.py'
extract_background_own_02 = 'extract_background_own_02.py'
extract_shape_color = 'extract_shape_color.py'
grabcut = 'grabcut.py'

# imagepath = sys.argv[1]
main_folder = '../images/pill_shapes/'
trials = ['trial'+str(x+1) for x in range(5)]
for shape in trials:
    imagepath = main_folder + shape + "/" + shape + '_front.jpg'

    # print("Running "+ edge_detect)
    # subprocess.check_output(['python', edge_detect, imagepath])
    # print("Running "+ extract_background_own)
    # subprocess.check_output(['python', extract_background_own, imagepath])
    print("Running "+ extract_background_own_02)
    subprocess.check_output(['python', extract_background_own_02, imagepath])
    # print("Running "+ grabcut)
    # subprocess.check_output(['python', grabcut, imagepath])
    input()
