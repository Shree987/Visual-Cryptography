## Adapted from https://tutorials.techonical.com/how-to-calculate-psnr-value-of-two-images-using-python/
import math
import os
import numpy as np
from PIL import Image

def psnr(original, contrast):
    mse = np.mean((original - contrast) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    PSNR = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return PSNR

def test_psnr():
    image = Image.open('../../Basic implementation/Shared key.png')
    contrast_image = Image.open('../../Basic implementation/Noise image.png')

    image = np.asarray(image)
    contrast_image = np.asarray(contrast_image)
    print(f"PSNR value is {psnr(image, contrast_image)} dB")


if __name__ == '__main__':
    test_psnr()