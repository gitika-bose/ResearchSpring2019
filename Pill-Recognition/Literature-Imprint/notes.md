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




-----
## Extra:

* Our algo won't work with rotation of images
* What is Grabcut? <br> From wiki:
> GrabCut is an image segmentation method based on graph cuts.
> Starting with a user-specified bounding box around the object to be segmented, the algorithm estimates the color distribution of the target object and that of the background using a Gaussian mixture model. This is used to construct a Markov random field over the pixel labels, with an energy function that prefers connected regions having the same label, and running a graph cut based optimization to infer their values. As this estimate is likely to be more accurate than the original, taken from the bounding box, this two-step procedure is repeated until convergence.
> Estimates can be further corrected by the user by pointing out misclassified regions and rerunning the optimization. The method also corrects the results to preserve edges.
*
