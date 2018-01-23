from . import simens_dadm as smns
import scipy.io as sio
from scipy import signal
from scipy.linalg import logm, expm
from scipy.fftpack import dct, idct
from scipy.special import iv
import numpy as np

def gauss2D(shape,sigma):

    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h
	
def filter2b(h,I0):

	Mx = np.size(h,1)
	My = np.size(h,0)
	Nx = (Mx-1)/2
	Ny = (My-1)/2
	Nx = int(float(Nx))
	Ny = int(float(Ny))
	It = np.pad(I0, [Nx, Ny], 'edge')
	filt = signal.convolve2d(It, np.rot90(h), mode='valid')
	return filt

def appro(z):
    cont = (z<1.5)
    z8 = np.multiply(8, z)
    z8[z==0] = 0.0001
    Mn = 1 - (3/z8) - (15/2/np.power(z8, 2)) - ((3*5*21)/6/np.power(z8, 3))
    Md = 1 + (1/z8) + (9/2/np.power(z8, 2)) + ((25*9)/6/np.power(z8, 3))
    M = Mn/Md
    M = M.flatten()
    i = 0
    if(sum(sum(cont))>1):
	    for x in np.nditer(z, op_flags=['readwrite']):
		    if x<1.5 and x!=0:
		        x[...] = (iv(1, x))/(iv(0, x))
		    elif x==0:
			    x[...] = 0
		    else:
			    x[...] = M[i]
		    i = i +1
    return z
	
def estimate_map(image):

    h1 = np.ones((5, 5))
    h1 /= 25
    local_mean = filter2b(h = h1, I0 = image)

    noise = image - local_mean

    x = np.size(image, 1)
    y = np.size(image, 0)
    Mask = np.ones((3, 3))
    Mask /= np.prod((3, 3))
    ak = filter2b(Mask, np.power(image, 2))
    ak = np.multiply(ak, 2)
    ak = np.power(ak, 2)
    ak = ak - filter2b(Mask, np.power(image, 4))
    ak[ak<0] = 0
    ak = np.sqrt(ak)
    ak = np.sqrt(ak)
    sigmak = filter2b(Mask, np.power(image, 2))
    sigmak = sigmak - np.power(ak, 2)
    sigmak[sigmak<0.01] = 0.01
    sigmak = np.multiply(sigmak, 0.5)
    for i in range(0,9):
        temp = np.multiply(ak, image)
        temp = temp/sigmak
        temp = appro(temp)
        temp = np.multiply(image, temp)
        temp = filter2b(Mask, temp)		
        ak = temp
        ak[ak<0] = 0		
        temp2 = abs(image)
        temp2 = np.power(temp2, 2)
        temp2 = filter2b(Mask, temp2)
        temp2 = np.multiply(0.5, temp2)
        temp3 = np.power(ak, 2)
        temp3 = np.multiply(0.5, temp3)
        temp2 = temp2-temp3
        sigmak = temp2
        sigmak[sigmak<0.01] = 0.01
    signal = ak
    sigman = np.sqrt(sigmak)
    SNR = signal/sigman	

    noise = abs(noise)

    noise = np.log(noise)

    x = np.size(noise, 1)
    y = np.size(noise, 0)
    h = gauss2D(shape = (2*x,2*y), sigma = (3.4*2))
    hmax = h.max()
    h /= hmax
    hx = np.size(h, 1)
    hy = np.size(h, 0)
    h = h[x:hx, y:hy]
    noise = dct(dct(noise, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')
    noise = np.multiply(noise, h)
    noise = idct(idct(noise, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')
    noise = np.real(noise)

    coefs = [-0.2895, -0.0389, 0.4099, -0.3552, 0.1493, -0.0358, 0.0050, -0.00037476, 0.000011802]
    correct = np.zeros((x,y))

    for i in range(0,8):
        correct = correct + np.multiply(coefs[i], np.power(SNR,i))
    temp = (SNR<=2.5)
    correct = np.multiply(correct, temp)
    noise = noise - correct
    
    x = np.size(noise, 1)
    y = np.size(noise, 0)
    h = gauss2D(shape = (2*x,2*y), sigma = ((3.4*2)+2.2))
    hmax = h.max()
    h /= hmax
    hx = np.size(h, 1)
    hy = np.size(h, 0)
    h = h[x:hx, y:hy]
    noise = dct(dct(noise, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')
    noise = np.multiply(noise, h)
    noise = idct(idct(noise, axis = 0, norm = 'ortho'), axis = 1, norm = 'ortho')
    noise = np.real(noise)

    noise = np.exp(noise)
	
    eg = 0.5772156649015328606/2
    noise = np.multiply(2, noise)
    noise /= np.sqrt(2)
    temp = np.exp(eg)
    noise = np.multiply(noise, temp)
    return noise

def main3(mri_input):

    if (isinstance(mri_input, smns.mri_diff)):
        [m, n, slices, gradients] = mri_input.diffusion_data.shape
        data_out = np.zeros([m, n, slices, gradients])

        for i in range(slices):
            for j in range(gradients):
                data_out_diff[:, :, i, j] = estimate_map(mri_input.diffusion_data[:, :, i, j])

        mri_input.diff_noise_map = data_out_diff
        
        [m, n, slices] = mri_input.structural_data.shape
        data_out = np.zeros([m, n, slices])

        for i in range(slices):
            data_out_struct[:, :, i] = estimate_map(mri_input.structural_data[:, :, i])

        mri_input.struct_noise_map = data_out_struct

    elif (isinstance(mri_input, smns.mri_struct)):
        [m, n, slices] = mri_input.structural_data.shape
        data_out = np.zeros([m, n, slices])

        for i in range(slices):
            data_out_struct[:, :, i] = estimate_map(mri_input.structural_data[:, :, i])

        mri_input.struct_noise_map = data_out_struct
    else:
        return "Unexpected data format in module number 0!"

    return mri_input	