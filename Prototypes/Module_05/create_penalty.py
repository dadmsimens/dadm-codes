import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math

def create_penalty(rsim):

    penalty = np.zeros([2 * rsim + 1, 2 * rsim + 1])
    for d in range(1, (rsim + 1)):
        value = 1 / (2*d+1)**2
        for i in range(-d, d+1):
            for j in range(-d, d+1):
                penalty[rsim - i, rsim - j] = penalty[rsim - i, rsim - j] + value
    penalty = penalty / rsim
    return penalty


def gauss_kernel(rsim):

    sigma = 1
    size = rsim * 2 + 1
    gauss1d = signal.gaussian(size, std=sigma).reshape(size, 1)
    gauss2d = np.outer(gauss1d, gauss1d)
    return gauss2d

# ploting the kernel
# plt.imshow(gauss_kernel(rsim), interpolation='none')
# plt.show()


def gk(rsim):

    penalty = np.zeros([2 * rsim + 1, 2 * rsim + 1])
    for d in range(1, (rsim + 1)):
        value = math.exp(-2*(d*d)/2) / (2 * 3.14)
        for i in range(-d, d+1):
            for j in range(-d, d+1):
                penalty[rsim - i, rsim - j] = penalty[rsim - i, rsim - j] + value
    penalty = penalty / rsim
    return penalty
