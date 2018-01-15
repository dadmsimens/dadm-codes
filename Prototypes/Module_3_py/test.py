import scipy.io as sio
from scipy import signal
from scipy.linalg import logm, expm
from scipy.fftpack import fft, dct, idct
from scipy.special import iv
import matplotlib.pyplot as plt
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
    z8[z==0] = 0.01
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
	
	
# load image
mat = sio.loadmat('In.mat')
In = mat['In']

# local mean
h1 = np.ones((5, 5))
h1 /= 25
local_mean = filter2b(h = h1, I0 = In)

# noise
noise = In - local_mean

# snr
x = np.size(In, 1)
y = np.size(In, 0)
Mask = np.ones((3, 3))
Mask /= np.prod((3, 3))
ak = filter2b(Mask, np.power(In, 2))
ak = np.multiply(ak, 2)
ak = np.power(ak, 2)
ak = ak - filter2b(Mask, np.power(In, 4))
ak[ak<0] = 0
ak = np.sqrt(ak)
ak = np.sqrt(ak)
sigmak = filter2b(Mask, np.power(In, 2))
sigmak = sigmak - np.power(ak, 2)
sigmak[sigmak<0.01] = 0.01
sigmak = np.multiply(sigmak, 0.5)
for i in range(0,9):
    temp = np.multiply(ak, np.power(In,2))
    temp = temp/sigmak
    temp = appro(temp)
    temp = filter2b(Mask, temp)
    ak = temp
    ak[ak<0] = 0
    temp2 = abs(In)
    temp2 = np.power(temp2, 2)
    temp2 = filter2b(Mask, temp2)
    temp2 /= 2
    temp2 = temp2 - np.multiply(0.5, np.power(ak, 2))
    sigmak = temp2
    sigmak[sigmak<0.01] = 0.01
signal = ak
sigman = np.sqrt(sigmak)
SNR = signal/sigman	

# abs
noise = abs(noise)

# log
noise = np.log(noise)

# lpf
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

# first correction
noise = noise + np.sqrt(2)
eg = 0.5772156649015328606/2
noise = noise + eg

# gaussian correction
coefs = [-0.2895, -0.0389, 0.4099, -0.3552, 0.1493, -0.0358, 0.0050, -3.7476e-04, 1.1802e-05]
correct = np.zeros((x,y))

#for i in range(0,7):
 #   correct = correct + np.multiply(coefs[i], np.power(SNR,i))
#noise = noise - correct

# exp
noise = np.exp(noise)
sio.savemat('gauss.mat', {'noise': noise})