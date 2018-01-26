import os
import time

from core.inc import simens_dadm as smns
from core.inc import module_06, module3, module_05, module08

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
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_06_test/'
DATASETS = {
    0: 'diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200'
}


if __name__ == '__main__':
    # API parameters (passed from GUI)
    dataset_name = DATASETS[0]
    solver = SOLVERS[0]
    fix_method = FIX_METHODS[0]

    # True to plot results
    plotting = True
    verbose = True
    pipeline = True

    # Load reconstructed data from file
    dwi = smns.load_object(file_path=DATASETS_ROOT+dataset_name)

    # Pre-procesing pipeline
    if pipeline is True:
        time.perf_counter()
        dwi = module3.main3(dwi)
        dwi = module_05.run_module(dwi)
        dwi = module08.main8(dwi, verbose=False)
        dwi.skull_stripping_mask = dwi.skull_stripping_mask == 1
        print("Module 3, 5, 8 (preprocessing) time: {} seconds.\n".format(time.perf_counter()))

    # Module 06 - Diffusion tensor estimation
    time.perf_counter()
    dwi = module_06.run_module(dwi, solver, fix_method, plotting, verbose)
    print("Module 6 (DTI) time: {} seconds.\n".format(time.perf_counter()))

    # Save object using pickle library
    if False:
        smns.save_object(file_path=DATASETS_ROOT+dataset_name, data_object=dwi)
