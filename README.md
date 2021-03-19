# Visual-Cryptography

**Visual Cryptography** is a cryptographic technique to encrypt visual information like images and text, which doesn’t require any sophisticated computation but a mere human sight-reading to decrypt. Visual Cryptography uses the idea of hiding secrets within images which are divided into multiple shares and then decoded by superimposing the shared images. 

This is a Visual Cryptography implementation as part of Cryptography course project (CS350 and CS353). In this project, the following methods are implemented based on the types of images: binary, grayscale, and colored. 
1. XOR implementation (Binary, Grayscale, and Colour)
2. Modular Arithmetic Implementation (Binary, Grayscale, and Colour)
3. Pixel expansion implementation (Binary)
4. Key + AES encryption implementation (Binary, Grayscale, and Colour)
5. Halftone CMYK Decomposition (Colour)
6. Bit-Level Decomposition (Grayscale)

We have planned to use PSNR (Peak Signal-to-Noise Ratio) and NCC (Normalized Cross-Correlation) as a metric to check how the final decrypted image is similar(or related) to the original image.

## Team Members
1.  [Shreeraksha R Aithal](https://github.com/Shree987) (181CO149)
2.  [K Krishna Swaroop](https://github.com/geekswaroop) (181CO125)

## Reference Materials
1. Papers
  * [Visual Cryptography](https://link.springer.com/content/pdf/10.1007/BFb0053419.pdf)
  * [Applications and usage of visual cryptography: A review](https://ieeexplore.ieee.org/document/7784984)
  * [Visual Cryptography for Gray-scale Images Using
Bit-level](http://bit.kuas.edu.tw/~jihmsp/2014/vol5/JIH-MSP-2014-01-010.pdf)
  * [An Implementation of Algorithms in Visual Cryptography in Images](http://www.ijsrp.org/research-paper-0313/ijsrp-p1574.pdf)
  * [Copyright protection scheme for digital images using visual cryptography and sampling methods](https://www.researchgate.net/publication/243483757_Copyright_protection_scheme_for_digital_images_using_visual_cryptography_and_sampling_methods)
  * [Visual Cryptography in Gray Scale Images](http://www.ijerd.com/paper/vol8-issue4/I08046568.pdf)
  * [A novel image encryption algorithm using AES and visual cryptography](https://ieeexplore.ieee.org/document/7877521)
  * [Visual cryptography for color images](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.457.5077&rep=rep1&type=pdf)
  * [Improving Image Quality In Extended Visual Cryptography For Halftone Images With No Pixel Expansion](http://www.ijstr.org/final-print/apr2014/Improving-Image-Quality-In-Extended-Visual-Cryptography-For-Halftone-Images-With-No-Pixel-Expansion.pdf)
