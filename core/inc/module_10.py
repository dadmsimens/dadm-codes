
# coding: utf-8

# In[1]:



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

def initial_interp(image, N, M):
    # initial interpolation
    interp_image = ndimage.zoom(image, N, mode='reflect')  # 512x512
    return(interp_image)

def Euclidean_dist(x1,y1,x2,y2):
    return(sqrt((x1-x2)**2+(y1-y2)**2))

def module10(image, N):
    window=2;
    image2 = initial_interp(image, N, N);
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
           
    return filtered_image
        


from . import simens_dadm as smns

def main10(mri_input, other_arguments = None):
    if (isinstance(mri_input, smns.mri_diff)): 
        print("This file contains diffusion MRI")
        [m, n, slices, gradients] = mri_input.diffusion_data.shape
        data_out = np.zeros([m, n, slices, gradients])
   
        for i in range(slices):
            for j in range(gradients):
                data_out[:, :, i, j] = module10(mri_input.diffusion_data[:, :, i, j])
        	
        mri_input.diffusion_data = data_out
        
    
    elif (isinstance(mri_input, smns.mri_struct)): 
        print("This file contains structural MRI")
        [m, n, slices] = mri_input.structural_data.shape
        data_out = np.zeros([m, n, slices])
        
        for i in range(slices):
            data_out[:, :, i] = module10(mri_input.structural_data[:, :, i], N)
        	
        mri_input.structural_data = data_out
        
    else:
        return "Unexpected data format in module number 10!"
    return mri_input

