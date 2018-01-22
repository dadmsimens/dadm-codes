import inc.module_10 as module10
import inc.simens_dadm as smns
import numpy as np
import matplotlib.pyplot as plt
from inc import simens_dadm as smns

#struct = smns.mri_read('../dane/dataset_T1')
FILE_PATH = '../dane/diffusion_synthetic_normal_L16_r2_slices_31_40_gr15_b1200'

mri_data = smns.load_object(file_path=FILE_PATH)
print(mri_data.structural_data.shape)
print(mri_data.diffusion_data.shape)

result10 = module_10.main10(mri_data)

[m, n, slices] = result10.structural_data.shape 
for i in range(slices):
    plt.imshow(result10.structural_data[:,:,i], cmap='gray')
plt.show()
