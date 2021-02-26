import numpy as np
import math
from scipy import signal
from PIL import Image

def normxcorr2D(image, template):
    t = np.asarray(template, dtype=np.float64)
    t = t - np.mean(t)
    norm = math.sqrt(np.sum(np.square(t)))
    t = t / norm

    sum_filter = np.ones(np.shape(t))


    a = np.asarray(image, dtype=np.float64)

    aa = np.square(a)

    a_sum = signal.correlate(a, sum_filter, 'same')
    aa_sum = signal.correlate(aa, sum_filter, 'same')

    numer = signal.correlate(a, t, 'same')

    denom = np.sqrt(aa_sum - np.square(a_sum)/np.size(t))

    tol = np.sqrt(np.finfo(denom.dtype).eps)
    nxcorr = np.where(denom < tol, 0, numer/denom)

    nxcorr = np.where(np.abs(nxcorr-1.) > np.sqrt(np.finfo(nxcorr.dtype).eps),nxcorr,0)

    return nxcorr

def psnr(original, contrast):
    mse = np.mean((original - contrast) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    PSNR = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return PSNR