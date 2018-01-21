import time

from core.inc import simens_dadm as smns
from core.inc import module_01

slice_idx = [5, 9]
FILE_PATH = 'dane/diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200'

# Load diffusion data
struct = smns.mri_read(FILE_PATH)

# Take only some slices
struct.diffusion_data = struct.diffusion_data[:, :, slice_idx, :, :]
struct.structural_data = struct.structural_data[:, :, slice_idx, :]

# Perform reconstruction
print("Starting Module 1 for {} slices...".format(len(slice_idx)))
time.perf_counter()
mri_data = module_01.run_module(struct)
print("Module 1 (Reconstruction) time: {} seconds.\n".format(time.perf_counter()))

# Save object using pickle library
smns.save_object(file_path=FILE_PATH, data_object=mri_data)
