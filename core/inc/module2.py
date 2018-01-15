import simens_dadm as smns
import numpy as np
import scipy.linalg
import scipy.io
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def normalizeMatrix(m):
    norm = ((m - np.min(m))/(np.max(m)-np.min(m)))
    return np.round(norm*255)+1

def rgb2gray(rgb):
    gray = np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    return gray

def gauss2D(shape=(170,170),sigma=2):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def func(data, a, b, c, d, e, f):
    return a+(b*data[:,0]**1)+(c*data[:,0]**2)+(d*data[:,1]**1)+(e*data[:,1]**2)+(f*data[:,1]**3)

def inhomogeneityCorrection(gray):
    sizex = gray.shape[0]
    sizey = gray.shape[1]
    
    kernelSize = np.int(np.floor((2 *sizex)/3))
    blurred = signal.fftconvolve(gray, gauss2D((kernelSize,kernelSize),kernelSize), mode='same')
    
    coordx = np.int64(np.ceil(np.random.random((1, 150)) * (sizex-1)))
    coordy = np.int64(np.ceil(np.random.random((1, 150)) * (sizey-1)))
    values = blurred[coordx, coordy]
    
    data = np.vstack([coordx, coordy, values]).T
    params, pcov = curve_fit(func, data[:,:2], data[:,2], method='lm')
    
    data2 = np.indices((sizex,sizey)).reshape(2,-1).T
    F = func(data2, *params)
    
    F = F.reshape(sizex, sizey)
    result = gray-F-np.mean(F)
	
    return result
  
def main2(mri_input, other_arguments = None):
    if (isinstance(mri_input, smns.mri_diff)): # instructions for diffusion mri
    
    # isinstance(mri_input, smns.mri_struct) returns TRUE for diffusion AND structural MRI because of inheritance.
    # It should be used if you have some code to work with BOTH structural and diffusion data (which may be frequent).
    
        mri_output = mri_input
        print("This file contains diffusion MRI")
    
    elif (isinstance(mri_input, smns.mri_struct)): # instructions specific for structural mri. The case of diffusion MRI is excluded here by elif.
        mri_output = inhomogeneityCorrection(mri_input)
        print("This file contains structural MRI")
    else:
        return "Unexpected data format in module number 0!"
    return mri_output