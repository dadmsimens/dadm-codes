import os
import unittest
import numpy as np
from core.inc import simens_dadm as smns
from core.inc import module_05


# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '\\Data\\Module_05_test\\'


class Module05Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Class initialization - data loading.
        """
        super(Module05Tests, cls).setUpClass()
        datasets = {
            0: DATASETS_ROOT + 'diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200',
            1: DATASETS_ROOT + ''
        }

        cls.data = smns.load_object(file_path=datasets[0])
        cls.data_const = smns.load_object(file_path=datasets[0])

    def tearDown(self):
        """
        Clearing the modifications made to data.
        """
        self.data.diffusion_data = self.data_const.diffusion_data
        self.data.noise_map = self.data_const.diffusion_data


    def test_empty_input_data(self):
        """
        What happens when algorithm encounters empty data.
        """
        self.data.diffusion_data = np.array([])
        self.assertRaises(ValueError, module_05.run_module,
                          self.data)

    def test_invalid_input_data(self):
        """
        What happens when algorithm encounters invalid data.
        """
        self.data.diffusion_data = self.data.diffusion_data[0]
        self.assertRaises(IndexError, module_05.run_module,
                          self.data)

    def test_size_check(self):
        """
        Checking the output size.
        """
        [x1, y1, s1, g1] = self.data.diffusion_data.shape
        [x2, y2, s2, g2] = module_05.run_module(self.data).shape
        self.assertEqual(x1, x2)
        self.assertEqual(y1, y2)
        self.assertEqual(s1, s2)
        self.assertEqual(g1, g2)

    def test_value_change(self):
        """
        Checking if function actually changes the values in images.
        """
        before = self.data.diffusion_data[:, :, 0, 0]
        after = module_05.run_module(self.data).diffusion_data[:, :, 0, 0]
        self.assertNotEqual(before, after)

    def test_map_absence(self):
        """
        What happens when algorithm encounters data with no noise maps.
        """
        self.data.noise_map = []
        self.assertRaises(ValueError, module_05.run_module,
                          self.data)

if __name__ == '__main__':
    unittest.main()
