# Modular Arithmetic implementation for Colour Image

import numpy as np
from PIL import Image
from ColourMetrics import psnr, normxcorr2D

def encrypt(input_image, share_size):
    image = np.asarray(input_image)
    (row, column, depth) = image.shape
    shares = np.random.randint(0, 256, size=(row, column, depth, share_size))
    shares[:,:,:,-1] = image.copy()
    for i in range(share_size-1):
        shares[:,:,:,-1] = (shares[:,:,:,-1] + shares[:,:,:,i])%256

    return shares, image

def decrypt(shares):
    (row, column, depth, share_size) = shares.shape
    shares_image = shares.copy()
    for i in range(share_size-1):
    	shares_image[:,:,:,-1] = (shares_image[:,:,:,-1] - shares_image[:,:,:,i] + 256)%256

    final_output = shares_image[:,:,:,share_size-1]
    output_image = Image.fromarray(final_output.astype(np.uint8))
    return output_image, final_output


if __name__ == "__main__":
    
    print("Save input image as 'Input.png' in the same folder as this file\n")

    try:
        share_size = int(input("Input the number of shares images you want to create for encrypting (min is 2, max is 8) : "))
        if share_size < 2 or share_size > 8:
            raise ValueError
    except ValueError:
    	print("Input is not a valid integer!")
    	exit(0)


    try:
        input_image = Image.open('Input.png')

    except FileNotFoundError:
    	print("Input file not found!")
    	exit(0)

    print("Image uploaded successfully!")
    print("Input image size (in pixels) : ", input_image.size)   
    print("Number of shares image = ", share_size)

    shares, input_matrix = encrypt(input_image, share_size)

    for ind in range(share_size):
        image = Image.fromarray(shares[:,:,:,ind].astype(np.uint8))
        name = "outputs/MA_Share_" + str(ind+1) + ".png"
        image.save(name)

    output_image, output_matrix = decrypt(shares)

    output_image.save('outputs/Output_MA.png')
    print("Image is saved 'Output_MA.png' ...")
    
    print("Evaluation metrics : ")    
    print(f"PSNR value is {psnr(input_matrix, output_matrix)} dB")
    print(f"Mean NCORR value is {normxcorr2D(input_matrix, output_matrix)}")