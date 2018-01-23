from core.inc import simens_dadm as smns
from core.inc import module_05
from core.inc import module3
import scipy.io as sio
import matplotlib.pyplot as plt
import os
import numpy as np


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_05_test/'
DATASETS = {
    0: 'diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200',
    1: 'filtered',
    2: 'noise'
}


if __name__ == "__main__":
    dataset_name = DATASETS[0]
    data = smns.load_object(file_path=DATASETS_ROOT + dataset_name)

    # set to 1 for first run (actually calculates map and filters images + saves results to pickles)
    if 0:
        data1 = module3.main3(data)
        smns.save_object(file_path=DATASETS_ROOT+'noise', data_object=data1)
        data2 = module_05.run_module(data1)
        smns.save_object(file_path=DATASETS_ROOT+'filtered', data_object=data2)

    real_example = 1
    if real_example:
        dataset_name = DATASETS[1]
        mri_data = smns.load_object(file_path=DATASETS_ROOT + dataset_name)

        noisy = data.diffusion_data[:, :, 1, 10]
        filtered = mri_data.diffusion_data[:, :, 1, 10]
        noise_map = mri_data.noise_map[:, :, 1, 10]

        fig = plt.figure()
        plt.subplot(1, 3, 1)
        plt.imshow(np.squeeze(noisy), cmap='gray')
        plt.axis('off')
        plt.title('noisy image')
        plt.subplot(1, 3, 2)
        plt.imshow(np.squeeze(noise_map), cmap='gray')
        plt.axis('off')
        plt.title('noise map')
        plt.subplot(1, 3, 3)
        plt.imshow(np.squeeze(filtered), cmap='gray')
        plt.axis('off')
        plt.title('UNLM result')
        plt.show()

    good_example = 0

    if good_example:
        scan = sio.loadmat(DATASETS_ROOT + 'imnoi.mat')['In']
        noise_map = sio.loadmat(DATASETS_ROOT + 'mapa.mat')['MapaR2']
        filtered_image = module_05.unlm(scan, noise_map)

        fig = plt.figure()
        plt.subplot(1, 3, 1)
        plt.imshow(np.squeeze(scan), cmap='gray')
        plt.axis('off')
        plt.title('noisy image')
        plt.subplot(1, 3, 2)
        plt.imshow(np.squeeze(noise_map), cmap='gray')
        plt.axis('off')
        plt.title('noise map')
        plt.subplot(1, 3, 3)
        plt.imshow(np.squeeze(filtered_image), cmap='gray')
        plt.axis('off')
        plt.title('UNLM effect')
        plt.show()
