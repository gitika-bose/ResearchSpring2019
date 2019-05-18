import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

img = cv2.imread(sys.argv[1])
w, h = img.shape[:2]

pixels = [tuple(img[x][y]) for x in range(w) for y in range(h)]

from sklearn.datasets.samples_generator import make_blobs
X, y_true = make_blobs(n_samples=300, centers=4,
                       cluster_std=0.60, random_state=0)
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.waitforbuttonpress()