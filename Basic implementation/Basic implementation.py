import numpy as np
from numpy import asarray
from PIL import Image

def encrypt(image, noise):
	'''Funtion to encrypt the input coloured image'''
	return (image + noise)%256
    
def decrypt(noise, secret):
	'''Funtion to decrypt and obtain the original coloured image'''
	return (secret-noise+256)%256

# Retrieving image
image = Image.open('Koala.jpg')			# Add the name of the required input image
print("Input image size (in pixels) : ", image.size)

# Show the image
image.show()

# Converting image to matrix
data = asarray(image)
print("Input image size (in terms of array dimensions) : ",data.shape)

# Creating noise image
noise = np.random.rand(data.size)
noise.resize(data.shape)
noise = ((noise*1000)%256).astype('uint8')

# Converting arrays back to images
data_image = Image.fromarray(data)		# Input image
noise_image = Image.fromarray(noise)	# Noise image


# Display the images obtained
#data_image.show()
#noise_image.show()

# Encrypt the original image
shared_key = encrypt(noise, data).astype(np.uint8)
shared_key_image = Image.fromarray(shared_key)
shared_key_image.show()

# Decrypt the final image to get inital image
original = decrypt(noise, shared_key).astype(np.uint8)
decrypted_image = Image.fromarray(original)
decrypted_image.show()

# Save the images
shared_key_image = shared_key_image.save('Shared key.png')
decrypted_image = decrypted_image.save('Final output.png')
noise_image = noise_image.save('Noise image.png')
print("All images are saved ...")