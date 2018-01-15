
# coding: utf-8

# In[2]:


import scipy as sc
import numpy as np
from numpy import * 
from scipy import * 
import scipy.io as scio
import matplotlib.pyplot as plt
from scipy import ndimage

matdata=scio.loadmat('recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat')
image=matdata['SENSE_LSE']
N=2 #extension

#initial interpolation
interp_image=ndimage.zoom(image, N, mode='reflect') #512x512
#spline interpolation, mode is what to do with boundries - the same as next row/column
#size of interpolation, it has to be the same horizontally and vertically


plt.imshow(image, cmap='gray') #256x256
plt.title('Original image')
plt.show()
plt.title('Spline interpolated image')
plt.imshow(interp_image, cmap='gray')





