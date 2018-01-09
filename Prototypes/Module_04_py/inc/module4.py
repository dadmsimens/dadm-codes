from . import simens_dadm as smns
import numpy as np
import scipy.signal as sig

def main4(mri_input, noise_map,image):

    if isinstance(mri_input, smns.mri_diff): # instructions for diffusion mri

        # isinstance(mri_input, smns.mri_struct) returns TRUE for diffusion AND structural MRI because of inheritance.
        # It should be used if you have some code to work with BOTH structural and diffusion data (which may be frequent).

        mri_output = mri_input
        print("This file contains diffusion MRI")


    elif (isinstance(mri_input, smns.mri_struct)):
        print("This file contains structural MRI")
        mri_input=image
        noise_map2 = np.power(noise_map, 2)
        image_4 = np.power(mri_input, 4)
        image_2 = np.power(mri_input, 2)
        window = np.ones((7, 7))
        Mn_4 = sig.convolve2d(image_4,window,'same')/49
        Mn_2 = sig.convolve2d(image_2,window,'same')/49
        K = 1 + (4 * np.power(noise_map2,2) - 4*noise_map2*Mn_2)/ (Mn_4 - np.power(Mn_2,2))
        im_est = Mn_2 - 2* noise_map2 + K * (image_2 - Mn_2)
        im_est = np.absolute(im_est)
        mri_input = np.sqrt(im_est)
    else:
        return "Unexpected data format in module number 4!"

    return mri_output