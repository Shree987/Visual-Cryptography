# Pixel Expansion implementation for Binary Image

import numpy as np
from PIL import Image
from BinaryMetrics import psnr, normxcorr2D

def extract_colour():
    colour = [[0,0,1,1], [1,1,0,0], [1,0,0,1],[0,1,1,0],[1,0,1,0],[0,1,0,1]]
    return np.array(colour[np.random.randint(0,6)])


def encrypt(input_image):
    input_matrix = np.asarray(input_image).astype(np.uint8)

    (row, column) = input_matrix.shape
    secret_share1 = np.empty((2*row, 2*column)).astype('uint8')
    secret_share2 = np.empty((2*row, 2*column)).astype('uint8')

    for i in range(row):
        for j in range(column):
            colour = extract_colour()
            secret_share1[2*i][2*j] = secret_share2[2*i][2*j] = colour[0]
            secret_share1[2*i + 1][2*j] = secret_share2[2*i + 1][2*j] = colour[1]
            secret_share1[2*i][2*j + 1] = secret_share2[2*i][2*j + 1] = colour[2]
            secret_share1[2*i + 1][2*j + 1] = secret_share2[2*i + 1][2*j + 1] = colour[3]

            if input_matrix[i][j] == 0:
                secret_share2[2*i][2*j] = 1 - secret_share2[2*i][2*j]
                secret_share2[2*i + 1][2*j] = 1 - secret_share2[2*i + 1][2*j]
                secret_share2[2*i][2*j + 1] = 1 - secret_share2[2*i][2*j + 1]
                secret_share2[2*i + 1][2*j + 1] = 1 - secret_share2[2*i + 1][2*j + 1] 

    return secret_share1, secret_share2, input_matrix


def decrypt(secret_share1, secret_share2, input_matrix):
    '''
    Black -> 0
    White -> 1

    White + White -> White ( 1 + 1 -> 1)
    White + Black -> Black ( 1 + 0 -> 0)
    Black + Black -> Black ( 0 + 0 -> 0)

    Best operator to use for this is - bitwise and
    
    '''
    matrix = secret_share1 & secret_share2
    (row, column) = secret_share1.shape
    row = int(row/2)
    column = int(column/2)
    output_matrix = np.ones((row, column))

    for i in range(row):
        for j in range(column):
            cnt = matrix[2*i][2*j] + matrix[2*i + 1][2*j] + matrix[2*i][2*j + 1] + matrix[2*i + 1][2*j + 1]
            if cnt == 0:
                output_matrix[i][j] = 0

    return output_matrix

if __name__ == "__main__":
    
    print("Save input image as 'Input.png' in the same folder as this file\n")

    try:
        input_image = Image.open('Input.png').convert('1')

    except FileNotFoundError:
        print("Input file not found!")
        exit(0)

    print("Image uploaded successfully!")
    print("Input image size (in pixels) : ", input_image.size)   
    print("Number of shares image = 2")

    secret_share1, secret_share2, input_matrix = encrypt(input_image)

    image1 = Image.fromarray(secret_share1.astype(np.uint8) * 255)
    image1.save("PE_SecretShare_1.png")
    image2 = Image.fromarray(secret_share2.astype(np.uint8) * 255)
    image2.save("PE_SecretShare_2.png")

    output_matrix = decrypt(secret_share1, secret_share2, input_matrix)
    output_image = Image.fromarray(output_matrix.astype(np.uint8) * 255)

    output_image.save('Output_PE.png', mode = '1')
    print("Image is saved 'Output_PE.png' ...")

    print("Evaluation metrics : ")    
    print(f"PSNR value is {psnr(input_matrix, output_matrix)} dB")
    print(f"NCORR value is {normxcorr2D(input_matrix, output_matrix)} shape")