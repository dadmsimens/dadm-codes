import os

from classes.mri_data import DiffusionData

# Module parameters definition, chosen later using GUI
SOLVERS = {
    0: 'wls',
    1: 'nls'
}
FIX_METHODS = {
    0: 'zero',
    1: 'abs',
    2: 'cholesky'
}

# Workaround for not implemented modules
DATASET_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\Module_06\\data\\'
DATASETS = {
    0: 'rec_35.mat',
    1: 'rec_40.mat',
    2: 'rec_48.mat'
}


if __name__ == '__main__':
    # API parameters (passed from GUI)
    dataset_name = DATASETS[1]
    solver = SOLVERS[0]
    fix_method = FIX_METHODS[1]
    plotting = True  # True for verifying functionality

    # Module 01 - Reconstruction
    dwi = DiffusionData(dataset_path=DATASET_ROOT + dataset_name)

    # Required preprocessing steps, currently a dummy method
    dwi.preprocess()

    # Module 08 - Skull stripping
    dwi.strip_skull()

    # Module 06 - Diffusion tensor estimation
    # biomarkers is a dictionary of biomarkers: MD, RA, FA, VR, FA_rgb
    dwi.get_dti_biomarkers(solver, fix_method, plotting)
