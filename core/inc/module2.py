from . import simens_dadm as smns
import numpy as np
import scipy.linalg
import scipy.io
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def gauss2D(shape=(170,170),sigma=10):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def func(data, a, b, c, d, e, f, g, h, i, j):
    return a+(b*data[:,0])+(c*data[:,1])+(d*(data[:,0]**2))+(e*(data[:,1]**2))+(f*(data[:,0]*data[:,1]))+(g*(data[:,0]**3))+(h*(data[:,1]**3))+(i*(data[:,0]**2)*data[:,1])+(j*(data[:,1]**2)*data[:,0])
 
def inhomogeneityCorrection(gray, mask):
    gray = gray*mask
    sizex = gray.shape[0]
    sizey = gray.shape[1]
    
    kernelSize = np.int(np.floor((2 *sizex)/3))
    blurred = signal.fftconvolve(gray, gauss2D((kernelSize,kernelSize),20), mode='same')
    
    coordx = np.int64(np.ceil(np.random.random((1, 150)) * (sizex-1)))
    coordy = np.int64(np.ceil(np.random.random((1, 150)) * (sizey-1)))
    values = blurred[coordx, coordy]
    data = np.vstack([coordx, coordy, values]).T
    
    params, pcov = curve_fit(func, data[:,:2], data[:,2])

    data2 = np.indices((sizex,sizey)).reshape(2,-1).T
    F = func(data2, *params)
    F = F.reshape(sizex, sizey)
    F[F < 1] = 1
    result = np.divide(gray, F+1e-8)
    return result
  
def main2(mri_input, other_arguments = None):
    if (isinstance(mri_input, smns.mri_diff)): # instructions for diffusion mri
        #print("This file contains diffusion MRI")
        [m, n, slices, gradients] = mri_input.diffusion_data.shape
        data_out = np.zeros([m, n, slices, gradients])
        # isinstance(mri_input, smns.mri_struct) returns TRUE for diffusion AND structural MRI because of inheritance.
        # It should be used if you have some code to work with BOTH structural and diffusion data (which may be frequent).
        for i in range(slices):
            for j in range(gradients):
                data_out[:, :, i, j] = inhomogeneityCorrection(mri_input.diffusion_data[:, :, i, j], mri_input.skull_stripping_mask[:, :, i, j])
        	
        mri_input.diffusion_data = data_out
        
    
    elif (isinstance(mri_input, smns.mri_struct)): # instructions specific for structural mri. The case of diffusion MRI is excluded here by elif.
        #print("This file contains structural MRI")
        [m, n, slices] = mri_input.structural_data.shape
        data_out = np.zeros([m, n, slices])
        
        for i in range(slices):
            data_out[:, :, i] = inhomogeneityCorrection(mri_input.structural_data[:, :, i], mri_input.skull_stripping_mask[:, :, i])
        	
        mri_input.structural_data = data_out
        
    else:
        return "Unexpected data format in module number 2!"
    return mri_input

