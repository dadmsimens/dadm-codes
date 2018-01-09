import inc.module4 as module4
import inc.simens_dadm as smns
import numpy as np
import scipy.io as sio
print("hello")
import matplotlib.pyplot as plt

struct = smns.mri_read('T1_synthetic_normal_1mm_L8_r2')
mat = sio.loadmat('test')
image = mat['In']
map = mat['MapaR2']
result1 = module4.main4(struct,map,image)

#visualization
fig = plt.figure()
plt.gray()  # show the filtered result in grayscale
ax1 = fig.add_subplot(121)  # left side
ax2 = fig.add_subplot(122)  # right side                   ax1.imshow(image)
ax2.imshow(result1)
ax1.imshow(image)
plt.show()
#print("Results:", result1.structural_data.shape)
#print(result1)
#for i in range(result1.diffusion_data.shape[-2]):
 #   print(result1.diffusion_data[:, :, i, :].shape)
# Print shapes of structural data array and all diffusion data directions

