import numpy as np
import os, sys
import base64
import hashlib
import pandas as pd
from PIL import Image
import scipy.misc
import matplotlib.pyplot as plt

# Reading input Image and encoding it using base64
with open("test2.jpg", "rb") as img_file:
    BI = base64.b64encode(img_file.read())
BI = BI.decode("utf-8")

## User Key
K = "Hello, World. ThisIsMyKey."

## Encode the key

SK = hashlib.sha256(K.encode()) 

print("The hexadecimal equivalent of SHA256 is : ") 
print(SK.hexdigest())


## AES Cipher

from Crypto.Cipher import AES
from Crypto.Random import new as Random
from hashlib import sha256
from base64 import b64encode,b64decode

class AESCipher:
    def __init__(self,data,key):
        self.block_size = 16
        self.data = data
        self.key = sha256(key.encode()).digest()[:32]
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr (self.block_size - len(s) % self.block_size)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self):
        plain_text = self.pad(self.data)
        iv = Random().read(AES.block_size)
        cipher = AES.new(self.key,AES.MODE_OFB,iv)
        return b64encode(iv + cipher.encrypt(plain_text.encode())).decode()
    
c = AESCipher(BI,SK.hexdigest()).encrypt()


## Encrypt Key as share
w = 255
h = len(K)
# creating new Image C of size(w,h) 
# initializing as blank
C = np.ones((h,w,1), dtype = 'uint8')

# Filling pixels in C
for i in range(h):
    j = ord(K[i])
    for k in range(w):
        if k < j:
            C[i][k][0] = 0
        else:
            break
            
# Dividing C into R and P
# initializing R and P of same size as C
R = np.ones((h,w,3), dtype = 'uint8')
P = np.ones((h,w,3), dtype = 'uint8')

for i in range(h):
    for j in range(w):
        r = np.random.normal(0,1,1)
        #print("r: ", r)
        R[i][j][0] = r

for i in range(h):
    for j in range(w):
        p = R[i][j][0] ^ C[i][j][0]
        P[i][j][0] = p
filename1 = 'shares/R.png'
filename2 = 'shares/P.png'
plt.imsave(filename1, R)
plt.imsave(filename2, P)

xdf = pd.DataFrame(columns = ['1','2'])
a = []
b = []
cnt = 0
for i in P:
    #print("I: ", i)
    #print("I Shape: ", i.shape)
    cnt+=1
    k = 0
    n1 = []
    n2 = []
    for j in i:
        #print("J SHape: ", j.shape)
        if k%2==0:
            n1.append(np.sum(j))
        else:
            n2.append(np.sum(j))
        k += 1    
    a.append(sum(n1))
    b.append(sum(n2))
# print("Cnt: ", cnt)
xdf['1'] = a
xdf['2'] = b

ydf = pd.DataFrame(columns = ['1','2'])
a = []
b = []
for i in R:
    k = 0
    n1 = []
    n2 = []
    for j in i:
        if k%2==0:
            n1.append(np.sum(j))
        else:
            n2.append(np.sum(j))
        k += 1    
    a.append(sum(n1))
    b.append(sum(n2))
ydf['1'] = a
ydf['2'] = b

from sklearn.linear_model import LinearRegression
LRmodel = LinearRegression()
LRmodel.fit(xdf,ydf)


zdf = pd.DataFrame(columns = ['1','2'])
a = []
b = []
for i in C:
    k = 0
    n1 = []
    n2 = []
    for j in i:
        if k%2==0:
            n1.append(np.sum(j))
        else:
            n2.append(np.sum(j))
        k += 1    
    a.append(sum(n1))
    b.append(sum(n2))
zdf['1'] = a
zdf['2'] = b

predict = LRmodel.predict([[sum(zdf['1']),sum(zdf['2'])]])

x = round(predict[0][0])%26
y = round(predict[0][1])%26

txt = []
for each in c:
    ch = ord(each) + x - y
    txt.append(int(ch))

text = ""
for t in txt:
    text += chr(t) + " "

f = open("shares/cipher2.txt",'a',encoding='utf-8')
f.write(text)
f.close()




########## DECRYPTION ##########

f = open("shares/cipher2.txt",'r',encoding='utf-8')
cipher = f.read()
P = plt.imread('shares/P.png')
R = plt.imread('shares/R.png')

h = np.shape(P)[0]
w = np.shape(P)[1]

CK = np.ones((h,w,1), dtype = 'uint8')

for i in range(h):
    for j in range(w):
        p = int(P[i][j][0])
        r = int(R[i][j][0])
        ck = np.bitwise_xor(p,r)
        CK[i][j][0] = ck

K1 = []
for i in range(len(CK)):
    K1.append(0)

for i in range(len(CK)):
    count = 0
    for j in range(len(CK[i])):
        if CK[i][j][0] == 0:
            count += 1
    K1[i] = chr(count)
K1 = "".join(K1)
print("Decrypted Key: ", K1)


SK1 = hashlib.sha256(K1.encode()) 

print("The hexadecimal equivalent of SHA256 is : ") 
print(SK1.hexdigest())


xdf = pd.DataFrame(columns = ['1','2'])
a = []
b = []
for i in P:
    k = 0
    n1 = []
    n2 = []
    for j in i:
        if k%2==0:
            n1.append(np.sum(j))
        else:
            n2.append(np.sum(j))
        k += 1    
    a.append(sum(n1))
    b.append(sum(n2))
xdf['1'] = a
xdf['2'] = b


ydf = pd.DataFrame(columns = ['1','2'])
a = []
b = []
for i in R:
    k = 0
    n1 = []
    n2 = []
    for j in i:
        if k%2==0:
            n1.append(np.sum(j))
        else:
            n2.append(np.sum(j))
        k += 1    
    a.append(sum(n1))
    b.append(sum(n2))
ydf['1'] = a
ydf['2'] = b


from sklearn.linear_model import LinearRegression

LRmodel = LinearRegression()
LRmodel.fit(xdf,ydf)

zdf = pd.DataFrame(columns = ['1','2'])
a = []
b = []
for i in CK:
    k = 0
    n1 = []
    n2 = []
    for j in i:
        if k%2==0:
            n1.append(np.sum(j))
        else:
            n2.append(np.sum(j))
        k += 1    
    a.append(sum(n1))
    b.append(sum(n2))
zdf['1'] = a
zdf['2'] = b

predict = LRmodel.predict([[sum(zdf['1']),sum(zdf['2'])]])


x = round(predict[0][0])%26
y = round(predict[0][1])%26

cipher = cipher.split(' ')

txt = []
for each in cipher:
    try:
        ch = ord(each) - x + y
        txt.append(int(ch))
    except:
        print(each)


text = ""
for t in txt:
    text += chr(t)

from Crypto.Cipher import AES
from Crypto.Random import new as Random
from hashlib import sha256
from base64 import b64encode,b64decode

class AESCipher:
    def __init__(self,data,key):
        self.block_size = 16
        self.data = data
        self.key = sha256(key.encode()).digest()[:32]
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr (self.block_size - len(s) % self.block_size)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def decrypt(self):
        cipher_text = b64decode(self.data.encode())
        iv = cipher_text[:self.block_size]
        cipher = AES.new(self.key,AES.MODE_OFB,iv)
        return self.unpad(cipher.decrypt(cipher_text[self.block_size:])).decode()
        
de = AESCipher(text,SK1.hexdigest()).decrypt()


de = de.encode("utf-8")

with open("DecryptedImg2.png", "wb") as fh:
    fh.write(base64.decodebytes(de))

