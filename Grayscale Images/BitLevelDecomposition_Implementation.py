# Pixel Expansion implementation for Binary Image

import numpy as np
from PIL import Image
from GrayscaleMetrics import psnr, normxcorr2D

def extract_colour():
    colour = [[0,0,1,1], [1,1,0,0], [1,0,0,1],[0,1,1,0],[1,0,1,0],[0,1,0,1]]
    return np.array(colour[np.random.randint(0,6)])


def PE_encrypt(input_matrix):

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

    return secret_share1, secret_share2


def PE_decrypt(secret_share1, secret_share2):
    '''
    Black -> 0
    White -> 1

    White + White -> White ( 1 + 1 -> 1)
    White + Black -> Black ( 1 + 0 -> 0)
    Black + White -> Black ( 0 + 1 -> 0)
    Black + Black -> Black ( 0 + 0 -> 0)

    Best operator to use for this is - bitwise and
    
    '''
    overlap_matrix = secret_share1 & secret_share2
    (row, column) = secret_share1.shape
    row = int(row/2)
    column = int(column/2)
    extraction_matrix = np.ones((row, column))

    for i in range(row):
        for j in range(column):
            cnt = overlap_matrix[2*i][2*j] + overlap_matrix[2*i + 1][2*j] + overlap_matrix[2*i][2*j + 1] + overlap_matrix[2*i + 1][2*j + 1]
            if cnt == 0:
                extraction_matrix[i][j] = 0

    return overlap_matrix, extraction_matrix


def convertGrayToBinary(image):
    grayScaleImage = image.copy()
    (row, column) = grayScaleImage.shape
    binaryImage = np.ones((row, column, 8))
    for i in range(8):
        binaryImage[:,:,i] = (grayScaleImage.copy())%2
        grayScaleImage = (grayScaleImage/2).astype('uint8')

    return binaryImage


def convertBinaryToGray(image):
    binaryImage = image.copy()
    (row, column, _) = binaryImage.shape
    grayScaleImage = np.zeros((row, column))
    for i in range(8):
        grayScaleImage = (grayScaleImage*2 + binaryImage[:,:,7-i]).astype('uint8')

    return grayScaleImage


def BLD_encrypt(input_image):
    input_matrix = np.asarray(input_image)
    binaryDecomposition = convertGrayToBinary(input_matrix.copy())

    (row, column, _) = binaryDecomposition.shape

    binaryShareImage_1 = np.zeros((2*row, 2*column, 8)).astype('uint8')
    binaryShareImage_2 = np.zeros((2*row, 2*column, 8)).astype('uint8')

    for index in range(8):
        binaryShareImage_1[:,:,index], binaryShareImage_2[:,:,index] = PE_encrypt(binaryDecomposition[:,:,index])

    secret_share1 = convertBinaryToGray(binaryShareImage_1)
    secret_share2 = convertBinaryToGray(binaryShareImage_2)

    return secret_share1, secret_share2, input_matrix


def BLD_decrypt(secret_share1, secret_share2):
    binaryShareImage_1 = convertGrayToBinary(secret_share1)
    binaryShareImage_2 = convertGrayToBinary(secret_share2)

    binaryShareImage_1 = binaryShareImage_1.astype('uint8')
    binaryShareImage_2 = binaryShareImage_2.astype('uint8')


    (row, column, _) = binaryShareImage_1.shape

    binaryOverlapMatrix = np.zeros((row, column, 8)).astype('uint8')
    binaryExtractionMatrix = np.zeros((int(row/2), int(column/2), 8)).astype('uint8')

    for index in range(8):
        binaryOverlapMatrix[:,:,index], binaryExtractionMatrix[:,:,index] = PE_decrypt(binaryShareImage_1[:,:,index], binaryShareImage_2[:,:,index])

    overlap_matrix = convertBinaryToGray(binaryOverlapMatrix)
    extraction_matrix = convertBinaryToGray(binaryExtractionMatrix)

    return overlap_matrix, extraction_matrix


if __name__ == "__main__":
    
    print("Save input image as 'Input.png' in the same folder as this file\n")

    try:
        input_image = Image.open('Input.png').convert('L')

    except FileNotFoundError:
        print("Input file not found!")
        exit(0)

    print("Image uploaded successfully!")
    print("Input image size (in pixels) : ", input_image.size)   
    print("Number of shares image = 2")

    secret_share1, secret_share2, input_matrix = BLD_encrypt(input_image)

    image1 = Image.fromarray(secret_share1.astype(np.uint8))
    image1.save("outputs/BLD_SecretShare_1.png")
    image2 = Image.fromarray(secret_share2.astype(np.uint8))
    image2.save("outputs/BLD_SecretShare_2.png")

    overlap_matrix, extraction_matrix = BLD_decrypt(secret_share1, secret_share2)
    extraction_output = Image.fromarray(extraction_matrix.astype(np.uint8))
    overlap_output = Image.fromarray(overlap_matrix.astype(np.uint8))

    extraction_output.save('outputs/Output_BLD(Extraction).png', mode = '1')
    print("Image is saved 'Output_BLD(Extraction).png' ...")

    overlap_output = overlap_output.resize(input_image.size)
    overlap_matrix = np.asarray(overlap_output).astype(np.uint8)
    overlap_output.save('outputs/Output_BLD(Overlap).png', mode = '1')
    print("Image is saved 'Output_BLD(Overlap).png' ...\n\n")

    print("Evaluation metrics for Extraction algorithm: ")    
    print(f"PSNR value is {psnr(input_matrix, extraction_matrix)} dB")
    print(f"Mean NCORR value is {normxcorr2D(input_matrix, extraction_matrix)}")

    print("\n\nEvaluation metrics for Overlap algorithm: ")    
    print(f"PSNR value is {psnr(input_matrix, overlap_matrix)} dB")
    print(f"Mean NCORR value is {normxcorr2D(input_matrix, overlap_matrix)}")

