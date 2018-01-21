import pickle

import scipy.io as sio
import numpy as np


class mri_struct:
    """A class for storing structural MRI data.

    structural_data is an array where the structural data are held (complex numbers)
    compression_rate is subsampling rate of the data (1 indicates no subsampling)
    coils_n is a number of coils used for data acquisition
    sensitivity_maps are sensitivity profiles of the coils

    noise_map is the estimated noise map
    skull_stripping_mask is a binary mask - the result of skull stripping module
    segmentation is a matrix with segmentation module result
    """

    def __init__(self, structural_data=None, compression_rate=1, coils_n=0, sensitivity_maps=None):
        self.structural_data = structural_data
        if self.structural_data.ndim==3:
            self.structural_data = np.expand_dims(structural_data, 2)
        self.compression_rate = compression_rate
        self.coils_n = coils_n
        self.sensitivity_maps = sensitivity_maps

        self.noise_map = []
        self.skull_stripping_mask = []
        self.segmentation = []


class mri_diff(mri_struct):
    """A class for storing diffusion MRI data.

    structural_data is an array where the structural data are held (complex numbers)
    compression_rate is subsampling rate of the data (1 indicates no subsampling)
    coils_n is a number of coils used for data acquisition
    sensitivity_maps are sensitivity profiles of the coils
    diffusion_data is the dMRI data
    gradients are directions of Diffusion MRI gradients
    b_value is the intensivity factor

    noise_map is the estimated noise map
    skull_stripping_mask is a binary mask - the result of skull stripping module
    segmentation is a matrix with segmentation module result
    biomarkers is the result of diffusion tensor imaging module
    """

    def __init__(self, raw_data, compression_rate=1, coils_n=0, sensitivity_maps=None, gradients=None, b_value=None):
        super().__init__(raw_data, compression_rate, coils_n, sensitivity_maps)
        if raw_data.ndim==4:
            raw_data = np.expand_dims(raw_data, 2)
        self.structural_data = np.take(raw_data, 0, axis=-2)

        self.diffusion_data = np.delete(raw_data, 0, axis=-2)
        self.gradients = gradients
        self.b_value = b_value

        self.biomarkers = list(dict())
        self.noise_map = []
        self.skull_stripping_mask = []


def mri_read(filename):
    mfile = sio.loadmat(filename)
    if ('raw_data' in mfile and 'r' in mfile and 'L' in mfile and 'sensitivity_maps' in mfile):
        if ('gradients' in mfile and 'b_value' in mfile):
            return mri_diff(raw_data=mfile['raw_data'], compression_rate=mfile['r'], coils_n=mfile['L'],
                            sensitivity_maps=mfile['sensitivity_maps'], gradients=mfile['gradients'],
                            b_value=mfile['b_value'])
        else:
            return mri_struct(structural_data=mfile['raw_data'], compression_rate=mfile['r'], coils_n=mfile['L'],
                              sensitivity_maps=mfile['sensitivity_maps'])
    else:
        return "Error: could not recognize data in file"

# TODO: ADD FUNCTIONS FOR EASY DATA ACCESS IN CLASSES.


def save_object(file_path, data_object):
    with open(file_path + '.pkl', 'wb') as output_path:
        pickle.dump(data_object, output_path, pickle.HIGHEST_PROTOCOL)

def load_object(file_path):
    with open(file_path + '.pkl', 'rb') as input_path:
        return pickle.load(input_path)
