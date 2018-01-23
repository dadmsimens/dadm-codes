import os
import unittest
import numpy as np
from core.inc import simens_dadm as smns
from core.inc import module_01


# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '\\Data\\Module_01_test\\'


class Module01Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Class initialization - data loading.
        """
        super(Module01Tests, cls).setUpClass()
        cls.datasets = {
            0: DATASETS_ROOT + 'T1_synthetic_normal_1mm_L8_r2',
        }
        cls.struct = smns.mri_read(file_path=cls.datasets[0])

    
    def tearDown(self):
        """
        Called after each testing method.
        Necessary because of input data test
        """
        self.struct = smns.mri_read(file_path=self.datasets[0])


    def test_none_input_data(self):
        """
        input structure lacks data.
        """
        invalid_struct = self.struct 
        invalid_struct.diffusion_data = np.array([])
        invalid_struct.structural_data = np.array([])
        self.assertRaises(ValueError, module_01.run_module, invalid_struct)

    def test_none_sensitivity_maps(self):
        """
        input structure lacks sensitivity maps profiles.
        """
        invalid_struct = self.struct
        invalid_struct.sensitivity_maps = np.array([])
        self.assertRaises(ValueError, module_01.run_module, invalid_struct)


    def test_invalid_input_subsampling_factor(self):
        """
        checks if function actually receives subsampling factor parameter
        """
        invalid_struct = self.struct
        invalid_struct.compression_rate = None
        self.assertRaises(ValueError, module_01.run_module, invalid_struct)

    def test_invalid_input_num_coils(self):
        """
        checks if function actually receives number of coils parameter
        """
        invalid_struct = self.struct
        invalid_struct.num_coils = None
        self.assertRaises(ValueError, module_01.run_module, invalid_struct)

if __name__ == '__main__':
    unittest.main()
