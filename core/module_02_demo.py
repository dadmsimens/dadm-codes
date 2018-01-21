import inc.module2 as module2
import inc.simens_dadm as smns
import numpy as np
import matplotlib.pyplot as plt

#struct = smns.mri_read('../dane/recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2')
FILE_PATH = '../dane/diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200'

mri_data = smns.load_object(file_path=FILE_PATH)
print(mri_data.structural_data.shape)
print(mri_data.diffusion_data.shape)

result2 = module2.main2(mri_data)

[m, n, slices] = result2.structural_data.shape 
for i in range(slices):
    plt.imshow(result2.structural_data[:,:,i], cmap='gray')
    plt.show()