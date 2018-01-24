from core.inc import simens_dadm as smns
from core.inc import module4
import matplotlib.pyplot as plt
import os
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '\\Data\\Module_04_test\\'
DATASETS = {
   0: 'noisemap'
}

if __name__ == "__main__":
    dataset_name = DATASETS[0]
    data = smns.load_object(file_path=DATASETS_ROOT + dataset_name)


    noisy = data.diffusion_data[:, :, 1, 10]
    print("start mod 4")
    data_fil=module4.main4(data)
    fil_image = data.diffusion_data[:, :, 1, 10]
    print("koniec")

    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(np.squeeze(noisy), cmap='gray')
    plt.axis('off')
    plt.title('noisy image')
    plt.subplot(1, 2, 2)
    plt.imshow(np.squeeze(fil_image), cmap='gray')
    plt.axis('off')
    plt.title('After LMMSE Estimation')
    plt.show()
