from . import module11_app as m11_app
import numpy as np

def main11(mri_input):
    '''check input data'''
    if type(mri_input.segmentation) != np.ndarray:
        raise ValueError('Incorrect type of input data from module 9')

    if mri_input.segmentation.ndim != 3 :
        raise ValueError('Incorrect dimension of input data from module 9')

    #seperation of cortex basing on segmentaion mask
    segmentation_data = mri_input.segmentation
    cortex_mask = segmentation_data != 3
    segmentation_data[cortex_mask]=0

    #initialization of new window
    myApp = m11_app.Brain3D_App(segmentation_data)

    return myApp

