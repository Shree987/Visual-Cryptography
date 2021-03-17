import numpy as np
import math
from scipy import signal
from PIL import Image

def normxcorr2D(image, template):
    """
    Normalized cross-correlation for 2D PIL images
    Adapted from: https://github.com/JustinLiang/ComputerVisionProjects/
    Inputs:
    ----------------
    template    The template. A PIL image.  Elements cannot all be equal.
    image       The PIL image.
    Output:
    ----------------
    nxcorr      Array of cross-correlation coefficients, in the range
                -1.0 to 1.0. Size == Input image and template shape
                Wherever the search space has zero variance under the template,
                normalized cross-correlation is undefined.
    """

    # (one-time) normalization of template
    t = np.asarray(template, dtype=np.float64)
    t = t - np.mean(t)
    norm = math.sqrt(np.sum(np.square(t)))
    if norm != 0:
        t = t / norm

    # create filter to sum values under template
    sum_filter = np.ones(np.shape(t))

    # get image
    a = np.asarray(image, dtype=np.float64)
    #also want squared values
    aa = np.square(a)

    # compute sums of values and sums of values squared under template
    a_sum = signal.correlate(a, sum_filter, 'same')
    aa_sum = signal.correlate(aa, sum_filter, 'same')
    # Note:  The above two lines could be made more efficient by
    #        exploiting the fact that sum_filter is separable.
    #        Even better would be to take advantage of integral images

    # compute correlation, 't' is normalized, 'a' is not (yet)
    numer = signal.correlate(a, t, 'same')
    # (each time) normalization of the window under the template
    denom = np.sqrt(aa_sum - np.square(a_sum)/np.size(t))

    # wherever the denominator is near zero, this must be because the image
    # window is near constant (and therefore the normalized cross correlation
    # is undefined). Set nxcorr to zero in these regions
    tol = np.sqrt(np.finfo(denom.dtype).eps)
    nxcorr = np.where(denom < tol, 0, numer/denom)

    # if any of the coefficients are outside the range [-1 1], they will be
    # unstable to small variance in a or t, so set them to zero to reflect
    # the undefined 0/0 condition
    nxcorr = np.where(np.abs(nxcorr-1.) > np.sqrt(np.finfo(nxcorr.dtype).eps),nxcorr,0)

    return np.mean(nxcorr)

def test_ncorr():
    
    image = Image.open('../Input.png')
    contrast_image = Image.open('../Output.png')
    print(f"Mean NCORR value is {normxcorr2D(image, contrast_image)}")

if __name__ == '__main__':
    test_ncorr()

