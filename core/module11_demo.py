import scipy.io as sio
import inc.module11 as module11
import inc.simens_dadm as smns
import os
import time


# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_11_test/'


if __name__ == "__main__":

    segmentation = sio.loadmat(DATASETS_ROOT + 'segmentationMask.mat')
    segmentation = segmentation['imageMaskFull']

    data = sio.loadmat(DATASETS_ROOT + 'originData.mat')
    data = data['imagesSkullFree']

    struct = smns.mri_struct()
    struct.structural_data = data
    struct.segmentation = segmentation
    result1 = module11.main11(struct)
