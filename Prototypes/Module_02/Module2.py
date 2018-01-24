import numpy as np
import scipy.linalg
import scipy.io
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def rgb2gray(rgb):
    gray = np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    return gray

def gauss2D(shape=(170,170),sigma=10):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

#mat = scipy.io.loadmat('dane/test.mat')
#gray = mat['I']

img = scipy.misc.imread('dane/brain2.png')
gray = rgb2gray(img)

#plt.imshow(gray, cmap='gray')
#plt.show()

sizex = gray.shape[0]
sizey = gray.shape[1]

size = np.int(np.floor((2 *sizex)/3))
blurred = signal.fftconvolve(gray, gauss2D((size, size),20), mode='same')

coordx = np.int64(np.ceil(np.random.random((1, 150)) * (sizex-1)))
coordy = np.int64(np.ceil(np.random.random((1, 150)) * (sizey-1)))
values = blurred[coordx, coordy]

data = np.vstack([coordx, coordy, values]).T

# # Curve fitting
# , k, l, m, n, o, p, q, r, s, t, u
def func(data, a, b, c, d, e, f, g, h, i, j):

    return a+(b*data[:,0])+(c*data[:,1])+(d*(data[:,0]**2))+(e*(data[:,1]**2))+(f*(data[:,0]*data[:,1]))+(g*(data[:,0]**3))+(h*(data[:,1]**3))+(i*(data[:,0]**2)*data[:,1])+(j*(data[:,1]**2)*data[:,0])
    #return a +(b*data[:,0])+( c*data[:,1] )+( d*data[:,0]**2 )+( e*data[:,0]*data[:,1] )+( f*data[:,1]**2 )+( g*data[:,0]**3 )+( h*data[:,0]**2*data[:,1] )+( i*data[:,0]*data[:,1]**2 )+( j*data[:,1]**3 )+( k*data[:,0]**4 )+( l*data[:,0]**3*data[:,1] )+( m*data[:,0]**2*data[:,1]**2 )+( n*data[:,0]*data[:,1]**3 )+( o*data[:,1]**4 )+( p*data[:,0]**5 )+( r*data[:,0]**4*data[:,1] )+( s*data[:,0]**3*data[:,1]**2 )+( t*data[:,0]**2*data[:,1]**3 )+( q*data[:,0]*data[:,1]**4 )+( u*data[:,1]**5)
params, pcov = curve_fit(func, data[:,:2], data[:,2])

data2 = np.indices((sizex,sizey)).reshape(2,-1).T
F = func(data2, *params)

F = F.reshape(sizex, sizey)

#gray[gray < 1] = 1
F[F < 1] = 1
result3 = np.divide(gray, F)-np.mean(F)
print(result3.max())
print(result3.min())
plt.imshow(gray, cmap='gray')
plt.show()
plt.imshow(blurred, cmap='gray')
plt.show()
plt.imshow(F, cmap='gray')
plt.show()
plt.imshow(result3, cmap='gray')
plt.show()