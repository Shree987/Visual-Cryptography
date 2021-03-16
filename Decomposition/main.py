from PIL import Image
import numpy as np
import random
import sys

######### CMYK Decomposition #########

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
print("CMYK Decomposition Done!")
outfile1.save('out1.jpg')
outfile2.save('out2.jpg')
outfile3.save('out3.jpg')

######### Halftone Conversion #########

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


print("Halftone Conversion Done!")
hf1.save('hf1.jpg')
hf2.save('hf2.jpg')
hf3.save('hf3.jpg')

######### Generate Shares #########

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


print("Generated Shares!")
share1.save('share1.jpg')
share2.save('share2.jpg')
share3.save('share3.jpg')


######### Combine Shares #########

infile1 = Image.open("share1.jpg")
infile2 = Image.open("share2.jpg")
infile3 = Image.open("share3.jpg")

outfile = Image.new('CMYK', infile1.size)

for x in range(0,infile1.size[0],2):
    for y in range(0,infile1.size[1],2):

        C = infile1.getpixel((x+1, y))[0]
        M = infile2.getpixel((x+1, y))[1]
        Y = infile3.getpixel((x+1, y))[2]


        outfile.putpixel((x, y), (C,M,Y,0))
        outfile.putpixel((x+1, y), (C,M,Y,0))
        outfile.putpixel((x, y+1), (C,M,Y,0))
        outfile.putpixel((x+1, y+1), (C,M,Y,0))

print("Combined Shares!")
outfile.save("final.jpg")