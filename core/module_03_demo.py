from core.inc import simens_dadm as smns
from core.inc import module3
import scipy.io as sio
import matplotlib.pyplot as plt
import os
import numpy as np


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_03_test/'
DATASETS = {
    0: 'diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200',
    1: 'noise',
}


if __name__ == "__main__":
    dataset_name = DATASETS[0]
    data = smns.load_object(file_path=DATASETS_ROOT + dataset_name)

    estimate = 0
    if estimate:
        data1 = module3.main3(data)
        smns.save_object(file_path=DATASETS_ROOT+'noise', data_object=data1)

    example = 1

    if example:
        dataset_name = DATASETS[1]
        mri_data = smns.load_object(file_path=DATASETS_ROOT + dataset_name)

        noisy = data.diffusion_data[:, :, 1, 10]
        noise_map = mri_data.diff_noise_map[:, :, 1, 10]

        fig = plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(np.squeeze(noisy), cmap='gray')
        plt.axis('off')
        plt.title('Noisy image')
        plt.subplot(1, 2, 2)
        plt.imshow(np.squeeze(noise_map))
        plt.axis('off')
        plt.title('Noise map')
        plt.show()