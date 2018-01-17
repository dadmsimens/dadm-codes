# coding: utf-8

# In[ ]:


import inc.module10 as module10
import inc.simens_dadm as smns
import numpy as np

#only for 2D input data
struct = smns.mri_read('dane/diffusion_synthetic_normal_L8_r2_gr15_b1200')
result1 = module10.main10(mriinput, N, M, plotting)
print("Results:", result1.structural_data.shape)
