## Generates shares from halftone images
from PIL import Image
import random
import sys
import numpy as np


image1 = Image.open("hf1.jpg")
image1 = image1.convert('CMYK')

image2 = Image.open("hf2.jpg")
image2 = image2.convert('CMYK')

image3 = Image.open("hf3.jpg")
image3 = image3.convert('CMYK')


share1 = Image.new("CMYK", [dimension * 2 for dimension in image1.size])

share2 = Image.new("CMYK", [dimension * 2 for dimension in image2.size])

share3 = Image.new("CMYK", [dimension * 2 for dimension in image3.size])




for x in range(0, image1.size[0]):
    for y in range(0, image1.size[1]):
        pixelcolor = image1.getpixel((x, y))

        if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
            share1.putpixel((x * 2, y * 2), (255,0,0,0))
            share1.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
            share1.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
            share1.putpixel((x * 2 + 1, y * 2 + 1), (255,0,0,0))

        else:
            share1.putpixel((x * 2, y * 2), (0,0,0,0))
            share1.putpixel((x * 2 + 1, y * 2), (255,0,0,0))
            share1.putpixel((x * 2, y * 2 + 1), (255,0,0,0))
            share1.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

        pixelcolor = image2.getpixel((x, y))

        if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
            share2.putpixel((x * 2, y * 2), (0,255,0,0))
            share2.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
            share2.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
            share2.putpixel((x * 2 + 1, y * 2 + 1), (0,255,0,0))

        else:
            share2.putpixel((x * 2, y * 2), (0,0,0,0))
            share2.putpixel((x * 2 + 1, y * 2), (0,255,0,0))
            share2.putpixel((x * 2, y * 2 + 1), (0,255,0,0))
            share2.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

        pixelcolor = image3.getpixel((x, y))

        if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
            share3.putpixel((x * 2, y * 2), (0,0,255,0))
            share3.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
            share3.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
            share3.putpixel((x * 2 + 1, y * 2 + 1), (0,0,255,0))

        else:
            share3.putpixel((x * 2, y * 2), (0,0,0,0))
            share3.putpixel((x * 2 + 1, y * 2), (0,0,255,0))
            share3.putpixel((x * 2, y * 2 + 1), (0,0,255,0))
            share3.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))



share1.save('share1.jpg')
share2.save('share2.jpg')
share3.save('share3.jpg')
