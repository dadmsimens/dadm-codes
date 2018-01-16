
# coding: utf-8

# In[3]:


import scipy as sc
import numpy as np
from numpy import *
from scipy import *
import scipy.io as scio
import matplotlib.pyplot as plt
from scipy import ndimage
import math

def initial_interp(image, N, M, display):
    # initial interpolation
    interp_image = ndimage.zoom(image, N, mode='reflect')  # 512x512
    # spline interpolation, mode is what to do with boundries - the same as next row/column
    # size of interpolation, it has to be the same horizontally and vertically
    if display == 1:
        plt.imshow(image, cmap='gray')  # 256x256
        plt.title('Original image')
        plt.show()
        plt.title('Spline interpolated image')
        plt.imshow(interp_image, cmap='gray')
        plt.show()
    return(interp_image)

def Euclidean_dist(x1,y1,x2,y2):
    return(sqrt((x1-x2)**2+(y1-y2)**2))

def upsampling(image, N, M, window, plotting):
    image2 = initial_interp(image, N, M, 0);
    s = image2.shape

    sigma = np.std(image2)
    level = sigma/2
    X, Y = np.meshgrid(range(-window, window), range(-window, window))
    tol = 0.002*sigma

    filtered_image = np.zeros(s);

    for i in range(1,s[0]):
        for j in range(1,s[1]):
            iMax = max(i-window,1)
            iMin = min(i+window,s[0])
            jMax = max(j-window,1)
            jMin = min(j+window,s[1])
            image_window = image2[iMax:iMin,jMax:jMin]


            #Intensity difference
            w1 = exp(-(np.absolute(image_window - image2[i, j])) ** 2 / (level ** 2))

            w2 = 0

            for k in range(iMax,iMin):
                for m in range(jMax,jMin):
                    w2 = exp((-Euclidean_dist(k, m, i, j))/level**2)


            weight = w1*w2
            iw = image_window[:]
            wx = weight[:]
            s1 = sum(wx*iw)
            s2 = sum(wx)
            filtered_image[i,j] = s1/s2

    image3 = []

    for i in np.arange(0,s[0],N):
        for j in np.arange(0,s[1],M):
            tmp = filtered_image[i:i+N-1,j:j+M-1]
            offset = image[int((i+N-1)/N),int((j+M-1)/M)] - np.mean(tmp[:])
            image3[i:int(i+N-1)][j:int(j+M-1)] = filtered_image[i:int(i+N-1)][j:int(j+M-1)] + offset
           

    if plotting==True:
        plt.imshow(image, cmap='gray')
        plt.title('Original image')
        plt.show()
        plt.imshow(filtered_image, cmap='gray')
        plt.title('Upsampled image')
        plt.show()
        

from . import simens_dadm as smns

def main10(mri_input, N, M, window, plotting=True):

    if (isinstance(mri_input, smns.mri_struct)):
        mri_output = upsampling(mri.input, N, M, window, plotting)
        print("This file contains structural MRI")
    else:
        return "Unexpected data format in module number 10!"

return mri_output

