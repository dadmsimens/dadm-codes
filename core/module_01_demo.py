import time

import inc.module_01 as module_01
import inc.simens_dadm as smns
import os
import matplotlib.pyplot as plt
import numpy as np

slice_idx = [5, 9]
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_01_test/'
#FILE_PATH = DATASETS_ROOT + 'T1_synthetic_normal_1mm_L8_r2'
FILE_PATH = DATASETS_ROOT + 'diffusion_synthetic_normal_L8_r2_slices_21_30_gr15_b1200'
# Load diffusion data
struct = smns.mri_read(FILE_PATH)

# Take only some slices
struct.diffusion_data = struct.diffusion_data[:, :, slice_idx, :, :]
struct.structural_data = struct.structural_data[:, :, slice_idx, :]
#struct.structural_data = struct.structural_data[:, :, :]

# Perform reconstruction
if __name__ == "__main__":
   
    reconstruction = 0
    
    if reconstruction:  
        print("Starting Module 1 for {} slice(s)...".format(len(slice_idx)))
        time.perf_counter()
        mri_data = module_01.run_module(struct)
        # Save object using pickle library
        smns.save_object(file_path=FILE_PATH, data_object=mri_data)
        print("Module 1 (Reconstruction) time: {} seconds.\n".format(time.perf_counter()))
        print("Module 1 (Reconstruction) data size:\n")
        print(mri_data.diffusion_data.shape)
        print("\n")
        print(mri_data.structural_data.shape)
        
    vizualization = 1

    if vizualization:
        FILE = 'diffusion_synthetic_normal_L8_r2_slices_21_30_gr15_b1200'
        mri_data = smns.load_object(file_path=DATASETS_ROOT + FILE)

        structural = mri_data.structural_data[:, :, 1]
        diffusion = mri_data.diffusion_data[:, :, 1, 5]

        fig = plt.figure()
        plt.subplot(1, 2, 1)
        plt.imshow(np.squeeze(structural), cmap='gray')
        plt.axis('off')
        plt.title('S0 image')
        plt.subplot(1, 2, 2)
        plt.imshow(np.squeeze(diffusion), cmap='gray')
        plt.axis('off')
        plt.title('Si image')
        plt.show()
    
'''
# To load the data later use:
mri_data = smns.load_object(file_path=FILE_PATH)
'''
