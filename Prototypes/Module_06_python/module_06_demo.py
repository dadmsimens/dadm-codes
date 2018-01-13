import os
import time

from inc import simens_dadm as smns
from inc import module_06

# Module parameters definition, chosen later using GUI
SOLVERS = {
    0: 'wls',
    1: 'nls'
}
FIX_METHODS = {
    0: 'abs',
    1: 'cholesky'
}

# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATASETS_ROOT = PROJECT_ROOT + '\\Data\\Module_06_test\\'
DATASETS = {
    0: 'rec_35.mat',
    1: 'rec_40.mat',
    2: 'rec_48.mat'
}


if __name__ == '__main__':
    # API parameters (passed from GUI)
    dataset_name = DATASETS[1]
    solver = SOLVERS[0]
    fix_method = FIX_METHODS[0]

    # True to plot results
    plotting = True

    # Dummy function to preprocess (implements other modules functionality)
    dwi = smns.mri_read_module_06(filename=DATASETS_ROOT + dataset_name)

    # Module 06 - Diffusion tensor estimation
    # dwi.biomarkers is a dictionary of biomarkers: MD, RA, FA, VR, FA_rgb
    time.perf_counter()
    dwi = module_06.run_module(dwi, solver, fix_method, plotting)
    print("Module 6 (DTI) time: {} seconds.\n".format(time.perf_counter()))
