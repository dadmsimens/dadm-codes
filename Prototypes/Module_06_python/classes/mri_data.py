
from abc import ABCMeta, abstractmethod

import os
import scipy.io
import numpy as np
import time

try:
    from .dti_solver_cy import run_module
    print('Using Cython implementation of module 6.')
except ImportError:
    from .dti_solver import run_module
    print('Using Python implementation of module 6.')


class Data:
    __metaclass__ = ABCMeta

    def __init__(self, dataset_path):
        pass

    @abstractmethod
    def _reconstruct(self, dataset_path):
        pass


class T2Data(Data):

    def __init__(self, dataset_path):
        super(T2Data, self).__init__(dataset_path)  # in case we're doing something in base class' Data.__init__
        # rest of constructor code
        # ...
        raise NotImplementedError('T2Data constructor not implemented.')

    def _reconstruct(self, dataset_path):
        raise NotImplementedError('Module 01 (Reconstruction) not implemented for T2Data.')


class DiffusionData(Data):

    MODULE_01_IMPLEMENTED = False
    MODULE_08_IMPLEMENTED = False
    PREPROCESSING_IMPLEMENTED = False

    def __init__(self, dataset_path):
        super(DiffusionData, self).__init__(dataset_path)  # in case we're doing something in base Data.__init__
        self._reconstruct(dataset_path)

    def _reconstruct(self, dataset_path):
        self.__dataset__ = dataset_path
        if DiffusionData.MODULE_01_IMPLEMENTED is True:
            raise NotImplementedError('Module 01 (Reconstruction) not implemented for DiffusionData.')
        else:
            print('RECONSTRUCT workaround: loading data from .mat files...\n')
            self.data, self.bvecs, self.bvals = self._load_matfile(dataset_path)
            self._check_bvecs()

    def preprocess(self):
        if DiffusionData.PREPROCESSING_IMPLEMENTED is True:
            raise NotImplementedError('Preprocessing modules not implemented for DiffusionData.')
        else:
            print('PREPROCESSING workaround: skipping...\n')

    def strip_skull(self):
        if DiffusionData.PREPROCESSING_IMPLEMENTED is True:
            raise NotImplementedError('Module 08 (Skull stripping) not implemented for DiffusionData.')
        else:
            print('SKULL STRIPPING workaround: loading from .mat file...\n')
            mask_path = os.path.dirname(self.__dataset__) + '\\mask.mat'
            matfile = scipy.io.loadmat(mask_path, struct_as_record=False, squeeze_me=True)
            self.mask = matfile['mask'] == 1

    def get_dti_biomarkers(self, solver, fix_method, plotting=False):
        time.perf_counter()
        self = run_module(self, solver, fix_method, plotting)
        print("Module 6 (DTI) time: {} seconds.\n".format(time.perf_counter()))

    def _load_matfile(self, dataset_path):
        """
        Helper function used to load and process data before Module 1 is implemented
        """
        matfile = scipy.io.loadmat(dataset_path, struct_as_record=False, squeeze_me=True)

        # data is not in correct range (can be negative); normalize to range <EPSILON, 1>
        EPSILON = 1e-8
        data = matfile['dwi'].data
        data_minimum = np.amin(data)
        data_maximum = np.amax(data)
        if not data_maximum-data_minimum == 0:
            data = EPSILON + (1-EPSILON) * (np.divide(data-data_minimum, data_maximum-data_minimum))
        else:
            raise ValueError('Data normalization results in division by zero.')

        return data, matfile['dwi'].bvecs, matfile['dwi'].bvals

    def _check_bvecs(self):
        EPSILON = 1e-4
        vector_norm = np.linalg.norm(self.bvecs, axis=1)
        if np.amin(vector_norm) <= 1-EPSILON or np.amax(vector_norm) >= 1+EPSILON:
            raise ValueError('BVECS should be an array of unit-length vectors.')