-----
## 10.1.1.443.4207

#### Methodology:
* Feature Extraction
* Feature Matching
* Feature Retrival

#### Pre-processing:
* Interpolation (Enhance size of image without modifying details of image, to give finer features)
  * Link: https://www.cambridgeincolour.com/tutorials/image-interpolation.htm
  * Bicubic Interpolation:
    * Bicubic considers the closest 4x4 neighborhood of known pixels — for a total of 16 pixels. Since these are at various distances from the unknown pixel, closer pixels are given a higher weighting in the calculation. Bicubic produces noticeably sharper images than bilinear or nearest neighbour, and is perhaps the ideal combination of processing time and output quality.
    * reduce blurring, error, jagged edges
  * Wavelet Interpolation
* Cropping Image

#### Feature Extraction:
##### Text
* Geometric gradient feature transformation algo
  * Query image --> input
  * Matched to database image using the algo


-----
## 06467032
[Pdf File](./06467032.pdf)
91% accurate.

* Shape
> represent the shape of a pill by using a shape distribution model sampled from the centroid of the drug. Given a mask M describing the location of the pill, the pixel distribution within the area is analyzed and used to estimate the center of mass C = {cx,cy}. By exploiting the fact that pills are convex objects, K equally spaced points P = {p1, p2, p3, . . . , pk} are estimated along the boundaries of the pill. Once the points are obtained, the Euclidean distance between the center C and each pi ∈ P is estimated and normalized. From the distance distribution, features such as the minimum, maximum, average, standard deviation, and roundness of the pill are estimated and used to describe shape. Note that such a feature is invariant to rotation, translation, scaling, and illumination changes.

* Imprint
> Given a mask M describing the location of the pill, morphological operations are used to estimate
Fig. 2. (top) A shape distribution model sampled from the centroid of the pill is used to capture shape properties. (bot- tom) An extension of shape distribution models is used to de- scribe imprint by only considering edge points.
M′, a reduced version of the original mask where M′ ≪ M. This step is done to reduce the high frequency signals often observed within the boundaries of an object. An edge map is estimated for the pill and masked by M′. Then, following the same steps as before, the center of mass C is estimated and K points along the boundaries of a pill are computed. For each pi ∈ P = {p1,p2,p3,...,pk}, the (C,pi) line is traversed and a set E = {e1, e2, . . . , ek} is estimated with the number of edge points found along each path. The number of edge points will correspond to the frequency of finding text, imprints, symbols, and engraves between the center and boundaries of the pill. Once E is normalized, features such as average, standard deviation, minimum, and maximum are used to describe the imprints of a drug in a scale and rotationally invariant approach.

* Color
>Given a mask M describing the position of the pill, the center of mass C is estimated and K points along the boundaries are computed. The pill image is converted to HSV to more effectively capture color changes. For each pi ∈ P = {p1,p2,p3,...,pk}, the (C,pi) line is traversed and each pixel value along the path (in the Hue and Saturation channels) are added to a list from where two 20-bin histograms are estimated. <br>
>To also capture color differences within the pill such as those caused by text and imprints, a second hue histogram is estimated for approximately one third of the pill closest to the center of mass. A mask M′ ≪ M was used to define the internal region of a pill to be considered for the imprint hue histogram.



-----
## Extra:

* Our algo won't work with rotation of images
* What is Grabcut? <br> From wiki:
> GrabCut is an image segmentation method based on graph cuts.
> Starting with a user-specified bounding box around the object to be segmented, the algorithm estimates the color distribution of the target object and that of the background using a Gaussian mixture model. This is used to construct a Markov random field over the pixel labels, with an energy function that prefers connected regions having the same label, and running a graph cut based optimization to infer their values. As this estimate is likely to be more accurate than the original, taken from the bounding box, this two-step procedure is repeated until convergence.
> Estimates can be further corrected by the user by pointing out misclassified regions and rerunning the optimization. The method also corrects the results to preserve edges.
*
