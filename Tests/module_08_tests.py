import os
import unittest
from unittest import mock
from unittest.mock import MagicMock
import numpy
import copy
from core.inc import simens_dadm as smns
from core.inc import module08


# Data location in ROOT
from core.inc.module08 import main8, SkullStripping

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_06_test/'
DATASETS = {
    0: 'diffusion_synthetic_normal_L8_r2_slices_41_50_gr15_b1200'
}

class Module08Tests(unittest.TestCase):

    def setUp(self):
        """
        Called once during test class initialization.
        Basically, you should place here your demo code (data loading). You should run your module in test methods.
        """
        dataset_name = DATASETS[0]
        self.dwi = smns.load_object(file_path=DATASETS_ROOT + dataset_name)


    def tearDown(self):
        """
        Called after each testing method.
        Might be necessary if your module modifies object in place.
        """
        pass

    def test_strel(self):
        ss = SkullStripping(None)
        se = ss.strel('disk', 1)
        disk = numpy.array([[1., 0., 1.], [0., 0., 0.], [1., 0., 1.]])
        self.assertEqual(type(se), type(disk))
        numpy.testing.assert_array_equal(se, disk)

    def test_radius_counting(self):
        ss = SkullStripping(None)
        se = ss.strel('disk', 6)
        r, st = ss.radius_counting(se)
        r_check = (6 * 2 + 1) / 2
        st_check = 1.0
        self.assertEqual(r, r_check)
        self.assertEqual(st, st_check)

    def test_binarization(self):
        ss = SkullStripping(None)
        image = numpy.array([[0.6, 0.7, 0.9], [0.2, 0.4, 0.3], [0.1, 0, 0.8]])
        threshold = 0.5
        bw_check = numpy.array([[1, 1, 1], [0, 0, 0], [0, 0, 1]])
        bw = ss.binarization(image, threshold)
        numpy.testing.assert_array_equal(bw, bw_check)

    def test_main8_incorrect_input(self):
        mri_input = None
        result = main8(mri_input)
        self.assertEqual(result, "Unexpected data format in module number 8!")

    @mock.patch("core.inc.module08.SkullStripping.preprocessing")
    def test_run_preprocessing_frist_condition(self, mock_obj):
        mock_obj.return_value = (None, None, None, 10, None)
        ss = SkullStripping(None)
        self.assertEqual(ss.run(), 0)
        mock_obj.return_value = (None, None, None, 100, 2.0)
        self.assertEqual(ss.run(), 0)


    def test_main8_adding_skull_stripping_mask(self):
        self.dwi.diff_skull_stripping_mask = []
        input_skull_stripping_mask = self.dwi.diff_skull_stripping_mask
        output_object = module08.main8(self.dwi)
        self.assertNotEqual(output_object.diff_skull_stripping_mask, input_skull_stripping_mask)

    def test_main08_not_changing_other_inputs(self):
         self.dwi.diff_skull_stripping = []
         inputs = copy.deepcopy(self.dwi.__dict__)
         output_object = module08.main8(self.dwi)
         inputs['diff_skull_stripping_mask'] = output_object.diff_skull_stripping_mask
         self.assertTrue(
             all(
                 [numpy.array_equal(inputs[key], getattr(output_object, key))
                  for key in inputs.keys()]
             )
         )

    def test_main08_mask_len_type(self):
        self.dwi.diff_skull_stripping_mask = numpy.zeros_like(self.dwi.diffusion_data[:, :, 0, 0])
        input_skull_stripping_mask = self.dwi.diff_skull_stripping_mask
        output_object = module08.main8(self.dwi)
        output_skull_stripping_mask = output_object.diff_skull_stripping_mask
        self.assertEqual(type(output_skull_stripping_mask), type(input_skull_stripping_mask))
        self.assertEqual(len(output_skull_stripping_mask), len(input_skull_stripping_mask))

if __name__ == '__main__':
    unittest.main()
