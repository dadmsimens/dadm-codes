from inc import simens_dadm as smns
from inc import module_05
import scipy.io as sio
import matplotlib.pyplot as plt
import os
import numpy as np


# works for one slice, so far
# getting data in silly manner

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_05_test/'


if __name__ == "__main__":
    scan = sio.loadmat(DATASETS_ROOT + 'imnoi.mat')['In']
    noise_map = sio.loadmat(DATASETS_ROOT + 'mapa.mat')['MapaR2']
    # filtering
    filtered_image = module_05.unlm(scan, noise_map)

    plot = 1
    if plot:
        fig = plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(np.squeeze(scan), cmap='gray')
        plt.axis('off')
        plt.title('noisy image')
        plt.subplot(1, 2, 2)
        plt.imshow(np.squeeze(filtered_image), cmap='gray')
        plt.axis('off')
        plt.title('UNLM effect')
        plt.show()
