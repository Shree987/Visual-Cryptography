# Halftone CMYK Decomposition for Colour Image

import numpy as np
from PIL import Image
from ColourMetrics import psnr, normxcorr2D

def CMYK_Decomposition(input_image):
    input_matrix = np.asarray(input_image)

    color_image = input_image.convert('CMYK')
    bw_image = input_image.convert('1')
    outfile1 = Image.new("CMYK", [dimension for dimension in input_image.size])
    outfile2 = Image.new("CMYK", [dimension for dimension in input_image.size])
    outfile3 = Image.new("CMYK", [dimension for dimension in input_image.size])


    for x in range(0, input_image.size[0], 1):
        for y in range(0, input_image.size[1], 1):
            sourcepixel = input_image.getpixel((x, y))
            outfile1.putpixel((x, y),(sourcepixel[0],0,0,0))
            outfile2.putpixel((x, y),(0,sourcepixel[1],0,0))
            outfile3.putpixel((x, y),(0,0,sourcepixel[2],0))

    outfile1.save('CMYK Share1_1.jpg')
    outfile2.save('CMYK Share1_2.jpg')
    outfile3.save('CMYK Share1_3.jpg')

    return input_matrix


def halftoneConversion():
    image1 = Image.open("CMYK Share1_1.jpg").convert('1')
    image2 = Image.open("CMYK Share1_1.jpg").convert('1')
    image3 = Image.open("CMYK Share1_1.jpg").convert('1')

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

    hf1.save('CMYK Share2_1.jpg')
    hf2.save('CMYK Share2_2.jpg')
    hf3.save('CMYK Share2_3.jpg')


def generateShares():
    image1 = Image.open('CMYK Share2_1.jpg').convert('CMYK')
    image2 = Image.open('CMYK Share2_2.jpg').convert('CMYK')
    image3 = Image.open('CMYK Share2_3.jpg').convert('CMYK')

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

    share1.save('CMYK Share3_1.jpg')
    share2.save('CMYK Share3_2.jpg')
    share3.save('CMYK Share3_3.jpg')


def combineShares():
    infile1 = Image.open('CMYK Share3_1.jpg')
    infile2 = Image.open('CMYK Share3_2.jpg')
    infile3 = Image.open('CMYK Share3_1.jpg')

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

    return outfile


if __name__ == "__main__":
    
    print("Save input image as 'Input.png' in the same folder as this file\n")

    try:
        input_image = Image.open('Input.png')

    except FileNotFoundError:
    	print("Input file not found!")
    	exit(0)

    print("Image uploaded successfully!")
    print("Input image size (in pixels) : ", input_image.size)   
    print("Number of shares image = ", 2)

    input_matrix = CMYK_Decomposition(input_image)
    halftoneConversion()
    generateShares()
    output_image = combineShares()

    output_image = output_image.resize(input_image.size)
    output_image.save('Output_CMYK.jpg', mode = "RGB")
    print("Image is saved 'Output_CMYK.jpg' ...")
    
    output_image = Image.open('Output_CMYK.jpg')
    if output_image.mode == 'CMYK':
        output_image = output_image.convert('RGB')
    output_matrix = np.asarray(output_image)
    
    print("Evaluation metrics : ")    
    print(f"PSNR value is {psnr(input_matrix, output_matrix)} dB")
    print(f"Mean NCORR value is {normxcorr2D(input_matrix, output_matrix)}")