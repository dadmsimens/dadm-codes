import os
from core.inc.module08 import SkullStripping, main8
from core.inc import simens_dadm as smns
import time
import scipy.io as sio
import os
from core.inc.module08 import SkullStripping, main8
from core.inc import simens_dadm as smns
import time
import scipy.io as sio


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_06_test/'
DATASETS = {
    0: 'diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200'
}

if __name__ == "__main__":
    dataset_name = DATASETS[0]
    dwi = smns.load_object(file_path=DATASETS_ROOT + dataset_name)
    time.perf_counter()
    dwi = main8(dwi, verbose=False)
    print("Module 8 time: {} seconds.\n".format(time.perf_counter()))

