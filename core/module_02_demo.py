import inc.simens_dadm as smns
import inc.module2 as module2
import inc.module08 as module08
import numpy as np
import matplotlib.pyplot as plt
import time

struct = smns.load_object('../Data/Module_02_test/T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2')
#struct.structural_data = struct.structural_data[:, :, slice_idx, :]
#print(struct.structural_data.shape)

# Perform bias field correction
struct = module08.main8(struct)
brain = module08.skull_stripped_image(struct) 

result2 = module2.main2(brain)

[m, n, slices] = result2.structural_data.shape 
for i in range(slices):
    plt.imshow(result2.structural_data[:,:,i], cmap='gray')
    plt.show()