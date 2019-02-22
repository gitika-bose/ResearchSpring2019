import subprocess
import sys

# canny_edge = 'canny_edge.py'
edge_detect = 'edge_detect.py'
extract_background_own = 'extract_background_own.py'
extract_background_own_02 = 'extract_background_own_02.py'
extract_shape_color = 'extract_shape_color.py'
grabcut = 'grabcut.py'

imagepath = sys.argv[1]

subprocess.check_output(['python', edge_detect, imagepath])
subprocess.check_output(['python', extract_background_own, imagepath])
subprocess.check_output(['python', extract_background_own_02, imagepath])
subprocess.check_output(['python', extract_shape_color, imagepath])
subprocess.check_output(['python', grabcut, imagepath])


