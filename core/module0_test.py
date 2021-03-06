import inc.module0_example as module0
import inc.simens_dadm as smns
import numpy as np

struct = smns.mri_read('dane/diffusion_synthetic_normal_L8_r2_slices_31_40_gr15_b1200')
result1 = module0.main0(struct)
print("Results:", result1.structural_data.shape)
for i in range(result1.diffusion_data.shape[-2]):
    if result1.diffusion_data.ndim==5:
        print(result1.diffusion_data[:, :, :, i, :].shape)
# Print shapes of structural data array and all diffusion data directions
print(result1.compression_rate, result1.noise_map)
print(result1.diffusion_data.shape)