# Modular Arithmetic implementation for Binary Image

import numpy as np
from PIL import Image

def encrypt(input_image, share_size):
    image = np.asarray(input_image)
    (row, column, depth) = image.shape
    shares = np.random.randint(0, 256, size=(row, column, depth, share_size))
    shares[:,:,:,-1] = image.copy()
    for i in range(share_size-1):
        shares[:,:,:,-1] = (shares[:,:,:,-1] + shares[:,:,:,i])%256

    return shares

def decrypt(shares):
    (row, column, depth, share_size) = shares.shape
    shares_image = shares.copy()
    shares_image[:,:,:,-1] = 255 - shares_image[:,:,:,-1]
    for i in range(share_size-1):
    	shares_image[:,:,:,-1] = shares_image[:,:,:,-1] + shares_image[:,:,:,i]

    final_output = shares_image[:,:,:,share_size-1]
    output_image = Image.fromarray(final_output.astype(np.uint8))
    return output_image


if __name__ == "__main__":
    
    print("Save input image as 'Input.png' in the same folder as this file\n")

    try:
        share_size = int(input("Input the number of shares images you want to create for encrypting (min is 2, max is 100) : "))
        if share_size < 2 or share_size > 100:
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

    shares = encrypt(input_image, share_size)

    output_image = decrypt(shares)

    output_image.save('Output_MA.png')
    print("Image is saved 'Output_MA.png' ...")