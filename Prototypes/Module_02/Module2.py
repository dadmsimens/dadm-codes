import numpy as np
import scipy.linalg
import scipy.io
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from blend_modes import blend_modes as bm

def normalizeMatrix(m):
    norm = ((m - np.min(m))/(np.max(m)-np.min(m)))
    return np.round(norm*255)+1

def rgb2gray(rgb):
    gray = np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    return gray

def gauss2D(shape=(170,170),sigma=2):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

# # Load image and gaussian filtering

mat = scipy.io.loadmat('../../dane/recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat')
gray = mat['SENSE_LSE']

sizex = gray.shape[0]
sizey = gray.shape[1]
sigmaValue = np.int(np.floor((2 *sizex)/3))

blurred = signal.fftconvolve(gray, gauss2D((sigmaValue,sigmaValue),30), mode='same')

# # 17 random points from the picture

coordx = np.int64(np.ceil(np.random.random((1, 17)) * (sizex-1)))
coordy = np.int64(np.ceil(np.random.random((1, 17)) * (sizey-1)))
values = blurred[coordx, coordy]

data = np.vstack([coordx, coordy, values]).T

# # Curve fitting

def func(data, a, b, c, d, e, f):
    return a+(b*data[:,0]**1)+(c*data[:,0]**2)+(d*data[:,1]**1)+(e*data[:,1]**2)+(f*data[:,1]**3)

params, pcov = curve_fit(func, data[:,:2], data[:,2], method='lm')

data2 = np.indices((sizex,sizey)).reshape(2,-1).T
F = func(data2, *params)

F = F.reshape(sizex, sizey)

#f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
plt.imshow(blurred, cmap='gray')
plt.show()
plt.imshow(F, cmap='gray')
plt.show()

plt.imshow(gray, cmap='gray')
plt.show()

#plt.imshow((gray/F), cmap='gray')
plt.imshow((gray-blurred+np.mean(blurred)), cmap='gray')
plt.show()

#plt.imshow((gray-F+np.mean(F)), cmap='gray')
#plt.show()


