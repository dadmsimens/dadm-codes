import os
import unittest
import numpy as np
import copy

from core.inc import simens_dadm as smns
from core.inc import module_06

# Data location in ROOT
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '\\Data\\Module_06_test\\'


class Module06Tests(unittest.TestCase):
    """
    Higher-level unit tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Called once during test class initialization.
        """
        super(Module06Tests, cls).setUpClass()
        cls.solvers = {
            0: 'wls',
            1: 'nls'
        }
        cls.fix_methods = {
            0: 'abs',
            1: 'cholesky'
        }
        cls.datasets = {
            0: DATASETS_ROOT + 'rec_35.mat',
            1: DATASETS_ROOT + 'rec_40.mat',
            2: DATASETS_ROOT + 'rec_48.mat'
        }

        # Dummy function to preprocess (implements other modules functionality)
        cls.dwi_input = smns.mri_read_module_06(filename=cls.datasets[0])

    def tearDown(self):
        """
        Called after each testing method.
        Necessary because module_06 modifies input object in place
        (self.dwi_input is a class member, so any changes will be present in all tests).
        """
        self.dwi_input.biomarkers = []

    """
    INTERFACE Tests 
    - testing behaviour when receiving incorrect data.
    """

    def test_invalid_input_data(self):
        invalid_data_instance = smns.mri_struct()
        self.assertRaises(ValueError, module_06.run_module,
                          invalid_data_instance, solver='wls', fix_method='abs')

    def test_invalid_solver_type(self):
        invalid_solver = 'wls_invalid'
        self.assertRaises(ValueError, module_06.run_module,
                          self.dwi_input, solver=invalid_solver, fix_method='abs')

    def test_invalid_fix_method_type(self):
        invalid_fix_method = 'abs_invalid'
        self.assertRaises(ValueError, module_06.run_module,
                          self.dwi_input, solver='wls', fix_method=invalid_fix_method)

    """
    DATA OBJECT Tests 
    - testing whether data instance is modified during module execution.
    """

    def test_object_modified_in_place(self):
        for solver in self.solvers.values():
            for fix_method in self.fix_methods.values():
                self.dwi_input.biomarkers = []
                output_object = module_06.run_module(self.dwi_input, solver=solver, fix_method=fix_method)
                self.assertEqual(self.dwi_input, output_object)

    def test_input_biomarker_field_changed(self):
        for solver in self.solvers.values():
            for fix_method in self.fix_methods.values():
                self.dwi_input.biomarkers = []
                input_biomarkers = self.dwi_input.biomarkers
                output_object = module_06.run_module(self.dwi_input, solver=solver, fix_method=fix_method)
                self.assertNotEqual(output_object.biomarkers, input_biomarkers)

    def test_input_other_fields_not_changed(self):
        for solver in self.solvers.values():
            for fix_method in self.fix_methods.values():
                self.dwi_input.biomarkers = []
                input_attributes = copy.deepcopy(self.dwi_input.__dict__)
                output_object = module_06.run_module(self.dwi_input, solver=solver, fix_method=fix_method)
                input_attributes['biomarkers'] = output_object.biomarkers
                self.assertTrue(
                    all(
                        [np.array_equal(input_attributes[key], getattr(output_object, key))
                         for key in input_attributes.keys()]
                    )
                )

    """
    OUTPUT Tests
    - testing whether output attribute (biomarkers) has expected properties.
    """

    def test_biomarker_fields_check(self):
        for solver in self.solvers.values():
            for fix_method in self.fix_methods.values():
                self.dwi_input.biomarkers = []
                markers_to_match = ['FA', 'MD', 'RA', 'VR', 'FA_rgb']
                output_object = module_06.run_module(self.dwi_input, solver=solver, fix_method=fix_method)
                output_object_markers = []
                for key in output_object.biomarkers[0].keys():
                    output_object_markers.append(key)
                self.assertEqual(set(output_object_markers), set(markers_to_match))

    def test_biomarkers_for_each_slice(self):
        for solver in self.solvers.values():
            for fix_method in self.fix_methods.values():
                self.dwi_input.biomarkers = []
                output_object = module_06.run_module(self.dwi_input, solver=solver, fix_method=fix_method)
                num_slices = np.shape(output_object.diffusion_data)[3]
                num_biomarkers = np.shape(output_object.biomarkers)[0]
                self.assertEqual(num_slices, num_biomarkers)

    def test_biomarker_shape(self):
        """
        Note: this method assumes that every input image slice has equal shape.
        Should be verified in separate unit test module.
        """
        for solver in self.solvers.values():
            for fix_method in self.fix_methods.values():
                self.dwi_input.biomarkers = []
                output_object = module_06.run_module(self.dwi_input, solver=solver, fix_method=fix_method)
                shape_test = []
                slice_dim = np.shape(output_object.structural_data)
                for marker in output_object.biomarkers[0].keys():
                    marker_dim = np.shape(output_object.biomarkers[0][marker])
                    if marker is 'FA_rgb':
                        shape_test.append(
                            len(marker_dim) == 3 and
                            marker_dim[0] == slice_dim[0] and marker_dim[1] == slice_dim[1] and marker_dim[2] == 3
                        )
                    else:
                        shape_test.append(
                            len(marker_dim) == 2 and
                            marker_dim[0] == slice_dim[0] and marker_dim[1] == slice_dim[1]
                        )
                self.assertTrue(all(shape_test))


class DTISolverTests(unittest.TestCase):
    """
    Lower-level unit tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Called once during test class initialization.
        """
        super(DTISolverTests, cls).setUpClass()
        cls.solvers = {
            0: 'wls',
            1: 'nls'
        }
        cls.fix_methods = {
            0: 'abs',
            1: 'cholesky'
        }
        cls.datasets = {
            0: DATASETS_ROOT + 'rec_35.mat',
            1: DATASETS_ROOT + 'rec_40.mat',
            2: DATASETS_ROOT + 'rec_48.mat'
        }

        # Dummy function to preprocess (implements other modules functionality)
        dwi = smns.mri_read_module_06(filename=cls.datasets[0])

        # Decompose input into objects
        slice_idx = 0

        structural_data = dwi.structural_data
        diffusion_data = dwi.diffusion_data
        data_merged = np.concatenate((structural_data, diffusion_data), axis=2)
        cls.data = np.squeeze(data_merged[:, :, :, slice_idx])

        cls.b_value = np.concatenate((np.zeros((np.shape(structural_data)[2])), dwi.b_value), axis=0)
        cls.gradients = np.concatenate((np.zeros((np.shape(structural_data)[2], 3)), dwi.gradients), axis=0)

        try:
            cls.mask = np.squeeze(dwi.skull_stripping_mask[:, :, :, slice_idx])
        except:
            # if mask is not defined for given slice
            cls.mask = []

    """
    CLASS SETUP Tests
    - validates the creation of DTISolver object.
    """

    def test_solver_object_created(self):
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=self.mask,
            solver='wls',
            fix_method='abs'
        )
        self.assertIsInstance(dti_solver, module_06.DTISolver)

    """
    INPUT Tests
    - validates handling of invalid input data (image, b_value, gradients).
    """

    def test_input_invalid_bvalue(self):
        invalid_bvalue = None
        self.assertRaises(ValueError, module_06.DTISolver,
                          data=self.data,
                          gradients=self.gradients,
                          b_value=invalid_bvalue,
                          mask=self.mask,
                          solver='wls',
                          fix_method='abs'
                          )

    def test_input_invalid_gradients(self):
        invalid_gradients = None
        self.assertRaises(ValueError, module_06.DTISolver,
                          data=self.data,
                          gradients=invalid_gradients,
                          b_value=self.b_value,
                          mask=self.mask,
                          solver='wls',
                          fix_method='abs'
                          )

    def test_input_invalid_data(self):
        invalid_data = None
        self.assertRaises(ValueError, module_06.DTISolver,
                          data=invalid_data,
                          gradients=self.gradients,
                          b_value=self.b_value,
                          mask=self.mask,
                          solver='wls',
                          fix_method='abs'
                          )

    def test_input_negative_data(self):
        negative_data = (-1) * self.data
        self.assertRaises(ValueError, module_06.DTISolver,
                          data=negative_data,
                          gradients=self.gradients,
                          b_value=self.b_value,
                          mask=self.mask,
                          solver='wls',
                          fix_method='abs'
                          )

    """
    SKULL STRIPPING MASK Tests
    - validates handling of an invalid skull stripping mask.
    """

    def test_input_skull_mask_empty(self):
        empty_mask = []
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=empty_mask,
            solver='wls',
            fix_method='abs'
        )
        self.assertEqual(np.amin(dti_solver._mask), True)

    def test_input_skull_mask_present(self):
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=self.mask,
            solver='wls',
            fix_method='abs'
        )
        self.assertEqual(np.amin(dti_solver._mask), False)

    def test_input_skull_mask_shape(self):
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=self.mask,
            solver='wls',
            fix_method='abs'
        )
        data_dims = np.shape(self.data)
        mask_dims = np.shape(dti_solver._mask)
        self.assertTrue(data_dims[0] == mask_dims[0] and data_dims[1] == mask_dims[1])

    def test_input_invalid_mask(self):
        invalid_mask = self.data
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=invalid_mask,
            solver='wls',
            fix_method='abs'
        )
        self.assertEqual(np.amin(dti_solver._mask), True)

    """
    GET_EIG Tests
    - validating computation of DTISolver.get_eig() method
    """

    def test_eigenvalues_abs_fix(self):
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=self.mask,
            solver='wls',
            fix_method='abs'
        )
        dti_solver.estimate_tensor()
        dti_solver.estimate_eig()
        eig_with_fix = np.amin(dti_solver._eig_image) >= 0

        dti_solver._fix_method = 'abs_invalid'
        dti_solver._tensor_image = (-1) * dti_solver._tensor_image
        dti_solver.estimate_eig()
        eig_without_fix = np.amin(dti_solver._eig_image) >= 0

        self.assertTrue((eig_with_fix == True) and (eig_without_fix == False))

    def test_eigenvalues_cholesky_fix(self):
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=self.mask,
            solver='wls',
            fix_method='cholesky'
        )
        dti_solver.estimate_tensor()
        dti_solver.estimate_eig()
        eig_with_fix = np.amin(dti_solver._eig_image) >= 0

        dti_solver._fix_method = 'cholesky_invalid'
        dti_solver.estimate_tensor()
        dti_solver.estimate_eig()
        eig_without_fix = np.amin(dti_solver._eig_image) >= 0

        self.assertTrue((eig_with_fix == True) and (eig_without_fix == False))

    """
    GET_BIOMARKERS Tests
    - validating computation of DTISolver.get_biomarkers() method
    """

    def test_negative_eigenvalue_biomarker_warning(self):
        dti_solver = module_06.DTISolver(
            data=self.data,
            gradients=self.gradients,
            b_value=self.b_value,
            mask=self.mask,
            solver='wls',
            fix_method='abs'
        )
        dti_solver.estimate_tensor()
        dti_solver.estimate_eig()
        dti_solver._eig_image = (-1) * dti_solver._eig_image
        self.assertWarns(RuntimeWarning, dti_solver.get_biomarkers)


if __name__ == '__main__':
    unittest.main()
