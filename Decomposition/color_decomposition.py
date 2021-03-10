## Takes in 3 dimensional colored image, outputs 4 dimensional CMYK(Cyan-Magenta-Yellow-Black image)
from PIL import Image
import numpy as np
import random
import sys


image = Image.open("doggo.jpg")
color_image = image.convert('CMYK')
bw_image = image.convert('1')


outfile1 = Image.new("CMYK", [dimension for dimension in image.size])

outfile2 = Image.new("CMYK", [dimension for dimension in image.size])

outfile3 = Image.new("CMYK", [dimension for dimension in image.size])



for x in range(0, image.size[0], 1):
    for y in range(0, image.size[1], 1):
        sourcepixel = image.getpixel((x, y))

        outfile1.putpixel((x, y),(sourcepixel[0],0,0,0))

        outfile2.putpixel((x, y),(0,sourcepixel[1],0,0))

        outfile3.putpixel((x, y),(0,0,sourcepixel[2],0))

outfile1.save('out1.jpg')
outfile2.save('out2.jpg')
outfile3.save('out3.jpg')
