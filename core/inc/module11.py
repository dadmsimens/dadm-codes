from . import module11_app as m11_app

def main11(mri_input):
    #seperation of cortex basing on segmentaion mask
    segmentation = mri_input.segmentation
    cortex_mask = segmentation != 3
    cortex_data = mri_input.structural_data
    cortex_data[cortex_mask] = 0

    #initialization of new window
    myApp = m11_app.Brain3D_App(cortex_data)
    return myApp

