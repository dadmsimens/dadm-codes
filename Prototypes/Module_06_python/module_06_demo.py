import os

from classes.mri_data import DiffusionData

# Module parameters
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
    dataset_path = DATASET_ROOT + DATASETS[1]

    # Module 01 - Reconstruction
    dwi = DiffusionData(dataset_path)

    # Required preprocessing steps, currently a dummy method
    dwi.preprocess()

    # Module 08 - Skull stripping
    dwi.strip_skull()

    # Module 06 - Diffusion tensor estimation
    solver = SOLVERS[0]
    fix_method = FIX_METHODS[1]
    dwi.estimate_tensor(solver, fix_method)

    print('fin')