# Visual Cryptography

**Visual Cryptography** is a cryptographic technique to encrypt visual information like images and text, which doesn’t require any sophisticated computation but a mere human sight-reading to decrypt. Visual Cryptography uses the idea of hiding secrets within images which are divided into multiple shares and then decoded by superimposing the shared images. 

In this project, the following methods are implemented based on the types of images: binary, grayscale, and colored. 
1. XOR implementation (Binary, Grayscale, and Colour)
2. Modular Arithmetic Implementation (Binary, Grayscale, and Colour)
3. Pixel expansion implementation (Binary)
4. Key + AES encryption implementation (Binary, Grayscale, and Colour)

We have planned to use PSNR (Peak Signal-to-Noise Ratio) and NCC (Normalized Cross-Correlation) as a metric to check how the final decrypted image is similar(or related) to the original image.
