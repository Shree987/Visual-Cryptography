## Takes the CMYK 3 dimensional decomposition and converts to halftone of the same size
from PIL import Image
import random
import sys
import numpy as np

image1 = Image.open("out1.jpg")
image2 = Image.open("out2.jpg")
image3 = Image.open("out3.jpg")

image1 = image1.convert('1')
image2 = image2.convert('1')
image3 = image3.convert('1')

hf1 = Image.new("CMYK", [dimension for dimension in image1.size])
hf2 = Image.new("CMYK", [dimension for dimension in image1.size])
hf3 = Image.new("CMYK", [dimension for dimension in image1.size])

for x in range(0, image1.size[0]):
    for y in range(0, image1.size[1]):
        pixel_color1 = image1.getpixel((x, y))
        pixel_color2 = image2.getpixel((x, y))
        pixel_color3 = image3.getpixel((x, y))
        if pixel_color1 == 255:
            hf1.putpixel((x, y),(255,0,0,0))
        else:
            hf1.putpixel((x, y),(0,0,0,0))

        if pixel_color2 == 255:
            hf2.putpixel((x, y),(0,255,0,0))
        else:
            hf2.putpixel((x, y),(0,0,0,0))

        if pixel_color3 == 255:
            hf3.putpixel((x, y),(0,0,255,0))
        else:
            hf3.putpixel((x, y),(0,0,0,0))



hf1.save('hf1.jpg')
hf2.save('hf2.jpg')
hf3.save('hf3.jpg')

