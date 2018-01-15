import os
from inc.module08 import SkullStripping
import scipy.io as sio


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_08_test/'


if __name__ == "__main__":
    image = DATASETS_ROOT + 'recon_T1_synthetic_normal_1mm_L8_r2.mat'
    # image = DATASETS_ROOT + 'recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat'
    # image = DATASETS_ROOT + 'SENSE_LSE_L_8_r_2_STD_2_RHO_0.mat'
    result_mask = SkullStripping(image).run(verbose=True)
