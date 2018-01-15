from . import simens_dadm as smns
import numpy as np
import scipy.signal as sig

def calculate_moments(image,window):
    image_4 = np.power(image, 4)
    image_2 = np.power(image, 2)
    Fourth_moment = sig.convolve2d(image_4, window, 'same') / window.size
    Second_moment = sig.convolve2d(image_2, window, 'same') / window.size

    return Second_moment, Fourth_moment
#calculate second order moment and fourth order moment by convolution image with square neighbourhood


def lmmse_filter(image,noise_map,window):
    noise_map2 = np.power(noise_map, 2)
    Mn_2, Mn_4 = calculate_moments(image,window)
    K = 1 + (4 * noise_map2**2 - 4 * noise_map2 * Mn_2) / (Mn_4 - Mn_2**2)
    filtered_image = Mn_2 - 2 * noise_map2 + K * (image**2 - Mn_2)
    filtered_image = np.absolute(filtered_image)
    filtered_image = np.sqrt(filtered_image)

    return filtered_image
#calcualte K parameters and estimate signal without noise

def main4(mri_input):

    if isinstance(mri_input, smns.mri_diff): # instructions for diffusion mri
        mri_output = mri_input
        window = np.ones((5, 5))
        for i in range(mri_input.diffusion_data.shape[2]):
            mri_output.diffusion_data[:, :, i] = lmmse_filter(mri_input.diffusion_data[:,:,i],mri_input.noise_map[:,:,i],window)
        print("This file contains diffusion MRI")
    #it should works, I make tests when 3D data will be available,

    elif (isinstance(mri_input, smns.mri_struct)):
        print("This file contains structural MRI")
        window = np.ones((5, 5))
        mri_output=mri_input
        mri_output.structural_data= lmmse_filter(mri_input.structural_data, mri_input.noise_map, window)

    else:
        return "Unexpected data format in module number 4!"

    return mri_output