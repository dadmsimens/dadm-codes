import os
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
        super().__init__(compression_rate, coils_n, sensitivity_maps)
        self.structural_data = raw_data[:, :, 0, :]

        self.diffusion_data = raw_data[:, :, 1:, :]
        self.gradients = gradients
        self.b_value = b_value

        self.biomarkers = dict()
        self.noise_map = []
        self.skull_stripping_mask = []


def mri_read(filename):
    mfile = sio.loadmat(filename)
    if ('raw_data' in mfile and 'r' in mfile and 'L' in mfile and 'sensitivity_maps' in mfile):
        if ('gradients' in mfile and 'b_value' in mfile):
            return mri_diff(mfile['raw_data'], mfile['r'], mfile['L'], mfile['sensitivity_maps'], mfile['gradients'],
                            mfile['b_value'])
        else:
            return mri_struct(mfile['raw_data'], mfile['r'], mfile['L'], mfile['sensitivity_maps'])
    else:
        return "Error: could not recognize data in file"

# TODO: ADD FUNCTIONS FOR EASY DATA ACCESS IN CLASSES.


def mri_read_module_06(filename):
    """
    Temporary wrapper loading reconstructed data while waiting for other modules to be implemented.
    Module 06 assumes reconstructed, preprocessed diffusion data, so a small wrapper is needed.
    """

    def _load_matfile(dataset_path):
        matfile = sio.loadmat(dataset_path, struct_as_record=False, squeeze_me=True)

        # data is not in correct range (can be negative); normalize to range <EPSILON, 1>
        EPSILON = 1e-8
        data = matfile['dwi'].data
        data_minimum = np.amin(data)
        data_maximum = np.amax(data)
        if not data_maximum - data_minimum == 0:
            data = EPSILON + (1 - EPSILON) * (np.divide(data - data_minimum, data_maximum - data_minimum))
        else:
            raise ValueError('Data normalization results in division by zero.')

        return data, matfile['dwi'].bvecs, matfile['dwi'].bvals

    def _check_bvecs(bvecs):
        EPSILON = 1e-4
        vector_norm = np.linalg.norm(bvecs, axis=1)
        if np.amin(vector_norm) <= 1 - EPSILON or np.amax(vector_norm) >= 1 + EPSILON:
            raise ValueError('BVECS should be an array of unit-length vectors.')

    def strip_skull(filename):
        try:
            mask_path = os.path.dirname(filename) + '\\mask.mat'
            matfile = sio.loadmat(mask_path, struct_as_record=False, squeeze_me=True)
            mask = matfile['mask'] == 1
            return mask
        except:
            print('Skull stripping mask not found!')
            return []

    try:
        data, bvecs, bvals = _load_matfile(filename)
        _check_bvecs(bvecs)
        mask = strip_skull(filename)

        dwi = mri_diff(
            raw_data=data[:, :, :, None],
            compression_rate=1,
            coils_n=0,
            sensitivity_maps=[],
            gradients=bvecs,
            b_value=bvals
        )
        # all modules compatibility
        dwi.structural_data = data[:, :, bvals == 0, None]
        dwi.diffusion_data = data[:, :, bvals != 0, None]
        dwi.b_value = bvals[bvals != 0]
        dwi.gradients = bvecs[bvals != 0]

        # try loading a mask
        dwi.skull_stripping_mask = mask

        return dwi

    except:
        raise ValueError("Error: could not recognize data in file")
