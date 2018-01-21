import unittest
import sys
import scipy.io as sio
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from core.inc import simens_dadm as smns
from core.inc import module11_model3D as model3D
from core.inc import module11
import vtk



class Module11Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Called once during test class initialization.
        Loading segmentation data
        """
        super(Module11Tests, cls).setUpClass()
        # Data loading
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_11_test/'
        cls.segmentation_data = sio.loadmat(DATASETS_ROOT + 'segmentationMask.mat')
        cls.segmentation_data = cls.segmentation_data['imageMaskFull']

        cls.struct = smns.mri_struct()
        cls.struct.segmentation = cls.segmentation_data


    def tearDown(self):
        """
        Called after each testing method.
        Necessary because of input data test
        """
        self.struct.segmentation = self.segmentation_data


    """
    INTERFACE Tests 
    - testing behaviour when receiving incorrect data.
    """
    def test_invalid_input_data_format(self):
        self.struct.segmentation = self.segmentation_data[1]
        self.assertRaises(ValueError, module11.main11,
                          self.struct)

    def test_invalid_input_data_type(self):
        self.struct.segmentation = None
        self.assertRaises(ValueError, module11.main11,
                          self.struct)


    """
    OUTPUT Test
    - validates output of reconstruction by marching cubes alghoritm
    """
    def test_generate_model(self):
        segmentation_data = self.struct.segmentation
        cortex_mask = segmentation_data != 3
        segmentation_data[cortex_mask]=0
        model = model3D.Model3D(segmentation_data)
        self.assertEqual(type(model.image), vtk.vtkImageData)
        self.assertEqual(type(model.model.GetOutput()), vtk.vtkPolyData)


if __name__ == '__main__':
    unittest.main()