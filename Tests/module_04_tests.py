import os
import unittest
import numpy as np
from core.inc import simens_dadm as smns
from core.inc import module4

# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '\\Data\\Module_04_test\\'
DATASETS = {
    0: 'noisemap'
}

class Module04Tests(unittest.TestCase):

    def setUp(self):
        dataset_name = DATASETS[0]
        self.data = smns.load_object(file_path=DATASETS_ROOT + dataset_name)

    def test_empty_input_data(self):
        """
        What happens when algorithm encounters empty data.
        """
        self.data.diffusion_data = np.array([])
        self.assertRaises(ValueError, module4.main4,
                          self.data)

    def test_incorrect_input_data(self):
        """
        What happens when algorithm encounters invalid data.
        """
        self.data.diffusion_data = self.data.diffusion_data[0]
        self.assertRaises(ValueError, module4.main4,
                          self.data)

    def test_size_input_data(self):
        """
        Checking the output size.
        """
        [x1, y1, s1, g1] = self.data.diffusion_data.shape
        output = module4.main4(self.data)
        [x2, y2, s2, g2] = output.diffusion_data.shape
        self.assertEqual(x1, x2)
        self.assertEqual(y1, y2)
        self.assertEqual(s1, s2)
        self.assertEqual(g1, g2)

    def test_none_noisemap(self):
        """
        What happens when algorithm encounters empty noisy map.
        """
        self.data.noise_map = []
        self.assertRaises(TypeError, module4.main4(self.data))

if __name__ == '__main__':
    unittest.main()
