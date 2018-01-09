cimport cython
import numpy as np
cimport numpy as np
import matplotlib.pyplot as plt
from cpython cimport array

#TODO: convert np.shape(X)[...] to X.shape?
#TODO: numpy matmul calls BLAS, which is coded in Fortran order
#TODO: cast for range indexes as Py_ssize_t

cdef class DWI:

    cdef double[:,:, ::1] data
    cdef double[:, ::1] bvecs
    cdef unsigned short[::1] bvals
    cdef unsigned short[:, ::1] mask

    def __cinit__(
            self,
            double[:,:, ::1] data,
            double[:, ::1] bvecs,
            unsigned short[::1] bvals,
            unsigned short[:, ::1] mask
        ):
        self.data = data
        self.bvecs = bvecs
        self.bvals = bvals
        self.mask = mask


cdef class DTISolver:

    # class variables
    cdef int MFN_MAX_ITER
    cdef double MFN_ERROR_EPSILON
    cdef double MFN_GRADIENT_EPSILON
    cdef str MFN_LAMBDA_MATRIX_FUN

    # __init__ parameters
    cdef DWI _dwi
    cdef str _solver
    cdef str _fix_method
    cdef double[:, ::1] _design_matrix

    # Setup MFN
    cdef int _max_iter
    cdef double _error_epsilon
    cdef double _gradient_epsilon
    cdef double[:, ::1] _lambda_matrix

    # TODO type definition
    # setup function handlers
    cdef object _solver_func
    cdef object _get_error_value
    cdef object _get_gradient
    cdef object _get_hessian

    # images
    cdef double[:,:, ::1] _tensor_image
    cdef double[:,:, ::1] _eig_image
    cdef double[:,:, ::1] _rgb_image
    cdef dict _biomarkers

    def __cinit__(
            self,
            DWI dwi,
            str solver,
            str fix_method
        ):

        # class variables
        self.MFN_MAX_ITER = 20
        self.MFN_ERROR_EPSILON = 1e-5
        self.MFN_GRADIENT_EPSILON = 1e-5
        self.MFN_LAMBDA_MATRIX_FUN = 'identity'

        # instance variables
        self._dwi = dwi
        self._solver = solver
        self._fix_method = fix_method

    def __init__(
            self,
            DWI dwi,
            str solver,
            str fix_method
        ):

        # get design matrix
        self._design_matrix = self._get_design_matrix()

        # initialize solvers
        self._setup_MFN()
        self._setup_solver()

    """
    Initialization
    """

    cdef double[:, ::1] _get_design_matrix(self):
        cdef double[:, ::1] design_matrix_temp
        cdef double[:, ::1] design_matrix

        design_matrix_temp = np.zeros((np.shape(self._dwi.bvals)[0], 6))
        design_matrix = np.ones((np.shape(self._dwi.bvals)[0], 7))

        design_matrix_temp = np.column_stack((
            np.square(self._dwi.bvecs[:, 0]),
            np.square(self._dwi.bvecs[:, 1]),
            np.square(self._dwi.bvecs[:, 2]),
            2 * np.multiply(self._dwi.bvecs[:, 0], self._dwi.bvecs[:, 1]),
            2 * np.multiply(self._dwi.bvecs[:, 1], self._dwi.bvecs[:, 2]),
            2 * np.multiply(self._dwi.bvecs[:, 0], self._dwi.bvecs[:, 2])
        ))

        design_matrix_temp *= np.multiply((-1), self._dwi.bvals[:, None])
        design_matrix[:,1:] = design_matrix_temp

        return design_matrix

    cdef void _setup_MFN(self):

        # MFN method convergence breakpoints
        self._max_iter = self.MFN_MAX_ITER
        self._error_epsilon = self.MFN_ERROR_EPSILON
        self._gradient_epsilon = self.MFN_GRADIENT_EPSILON

        # Lambda parameter to multiply the hessian
        if self.MFN_LAMBDA_MATRIX_FUN == 'identity':
            self._lambda_matrix = np.eye(7)

        if self._fix_method == 'cholesky':
            self._get_cholesky_P_matrix()

    cdef void _setup_solver(self):

        # TODO: convert function pointers
        if self._solver == 'wls':
            self._solver_func = self._solve_wls
            self._get_error_value = self._get_wls_error_value
            self._get_gradient = self._get_wls_gradient
            self._get_hessian = self._get_wls_hessian

            if self._fix_method == 'cholesky':
                self._solver_func = self._solve_nls

        # TODO: convert function pointers
        elif self._solver == 'nls':
            self._solver_func = self._solve_nls
            self._get_error_value = self._get_nls_error_value
            self._get_gradient = self._get_nls_gradient
            self._get_hessian = self._get_nls_hessian

        else:
            raise ValueError('Invalid DTI SOLVER type.')

    """
    Solvers
    """

    cdef double[:, ::1] _build_tensor(self, double[::1] tensor_vector):
        cdef double[:, ::1] tensor = np.zeros((3, 3))

        # x-row
        tensor[0, 0] = tensor_vector[0]
        tensor[0, 1] = tensor_vector[3]
        tensor[0, 2] = tensor_vector[5]

        # y-row
        tensor[1, 0] = tensor_vector[3]
        tensor[1, 1] = tensor_vector[1]
        tensor[1, 2] = tensor_vector[4]

        # z-row
        tensor[2, 0] = tensor_vector[5]
        tensor[2, 1] = tensor_vector[4]
        tensor[2, 2] = tensor_vector[2]

        return tensor

    cdef double[:,:, ::1] _pixel_loop(self,
            unsigned int image_depth,
            function_handle
            ):
        cdef double [:,:, ::1] output_image
        cdef unsigned int id_x, id_y
        cdef double[::1] temp

        output_image = np.zeros((np.shape(self._dwi.data)[0], np.shape(self._dwi.data)[1], image_depth))

        # very naive implementation
        for id_x in range(np.shape(self._dwi.data)[0]):
            for id_y in range(np.shape(self._dwi.data)[1]):

                if self._dwi.mask[id_x, id_y]:
                    #TODO: temp?
                    temp = function_handle(self, id_x, id_y)
                    output_image[id_x, id_y, :] = temp

            if not np.floor(100*id_x/np.shape(self._dwi.data)[0]) % 10:
                print('Progress: {0:0.2f}%'.format(100*id_x/np.shape(self._dwi.data)[0]))

        return output_image

    cdef void estimate_tensor(self):
        # TODO:
        cdef unsigned int image_depth = 6

        # TODO: this declaration should be somewhere else, convert function pointers
        def estimate_tensor_pixel_func(DTISolver self, unsigned int id_x, unsigned int id_y):

            cdef double[::1] pixel
            cdef double[::1] estimate

            pixel = np.squeeze(self._dwi.data[id_x, id_y, :])
            estimate = self._solver_func(pixel)
            return estimate[1:]

        self._tensor_image = self._pixel_loop(image_depth, estimate_tensor_pixel_func)

    cdef void estimate_eig(self):
        cdef double[:,:, ::1] results
        cdef unsigned int image_depth = 6

        #TODO
        def estimate_eig_pixel_func(DTISolver self, unsigned int id_x, unsigned int id_y):
            tensor = self._build_tensor(np.squeeze(self._tensor_image[id_x, id_y, :]))
            eig_vals, eig_vectors = np.linalg.eigh(tensor)

            # eigenvalues in ascending order, flip array
            eig_vals = eig_vals[::-1]

            # get RGB values (from eigenvectr corresponding to largest eigenvalue)
            # red: transversal (left-right)
            # green: anterior-posterior (front-back)
            # blue: cranio-caudal (head-feet)
            # we take absolute value because we care about the axis in general, not direction specifically
            rgb = np.abs(eig_vectors[:, -1])

            if self._fix_method == 'zero':
                eig_vals[eig_vals < 0] = 0
            elif self._fix_method == 'abs':
                eig_vals = np.abs(eig_vals)

            return np.hstack((eig_vals, rgb))

        results = self._pixel_loop(image_depth, estimate_eig_pixel_func)

        # split results into eigenvalues and rgb map
        self._eig_image = results[:, :, 0:3]
        self._rgb_image = results[:, :, 3:]

    """
    Biomarkers
    """

    #TODO
    cpdef dict get_biomarkers(self):
        MD = self._get_marker_MD()
        RA = self._get_marker_RA()
        FA = self._get_marker_FA()
        VR = self._get_marker_VR()
        FA_rgb = np.multiply(FA[:, :, None], self._rgb_image)

        biomarkers = {
            'MD': MD,
            'RA': RA,
            'FA': FA,
            'VR': VR,
            'FA_rgb': FA_rgb
        }

        self._biomarkers = biomarkers
        return biomarkers

    #TODO
    cpdef _get_marker_MD(self):
        return np.mean(self._eig_image, axis=2)

    #TODO
    cpdef _get_marker_RA(self):
        mask = np.array(self._dwi.mask) > 0.01
        MD = self._get_marker_MD()
        eig_variance = self._get_eig_variance()

        RA = np.zeros(np.shape(MD))
        RA[mask] = np.sqrt(np.divide(eig_variance[mask], np.multiply(3, MD[mask])))
        return RA

    #TODO
    cpdef _get_marker_FA(self):
        mask = np.array(self._dwi.mask) > 0.01

        eig_variance = self._get_eig_variance()
        sum_squares = np.sum(np.square(self._eig_image), axis=2)

        FA = np.zeros(np.shape(eig_variance))
        FA[mask] = np.multiply(np.sqrt(3/2), np.sqrt(np.divide(eig_variance[mask], sum_squares[mask])))
        return FA

    #TODO
    cpdef _get_marker_VR(self):
        mask = np.array(self._dwi.mask) > 0.01

        MD = self._get_marker_MD()

        VR = np.zeros(np.shape(MD))
        VR[mask] = np.divide(
            (np.prod(self._eig_image, axis=2))[mask], np.power(MD[mask], 3)
        )
        return VR

    #TODO
    cpdef _get_eig_variance(self):
        MD = self._get_marker_MD()
        return np.sum(np.square(np.subtract(self._eig_image, MD[:, :, None])), axis=2)

    """
    Plotting (debug)
    """

    #TODO
    def plot_tensor(self):
        plot_dict = {
            331: [0, 'Dxx'],
            332: [3, 'Dxy'],
            333: [5, 'Dxz'],
            334: [3, 'Dyx'],
            335: [1, 'Dyy'],
            336: [4, 'Dyz'],
            337: [5, 'Dzx'],
            338: [4, 'Dzy'],
            339: [2, 'Dzz'],
        }
        fig = plt.figure()
        plt.suptitle('Diffusion tensor estimate')

        for key, value in plot_dict.items():
            plt.subplot(key)
            plt.imshow(np.squeeze(self._tensor_image[:, :, value[0]]), cmap='gray')
            plt.axis('off')
            plt.title(value[1])

    #TODO
    def plot_eig(self):
        plot_dict = {
            131: [0, r'$\lambda_1$'],
            132: [1, r'$\lambda_2$'],
            133: [2, r'$\lambda_3$'],
        }
        fig = plt.figure()
        plt.suptitle('Diffusion tensor estimate eigenvalue images')

        for key, value in plot_dict.items():
            plt.subplot(key)
            plt.imshow(np.squeeze(self._eig_image[:, :, value[0]]), cmap='gray')
            plt.axis('off')
            plt.title(value[1])

    #TODO
    def plot_biomarkers(self):
        plot_dict = {
            221: ['MD', 'MD (Mean Diffusivity)'],
            222: ['RA', 'RA (Relative Anisotropy)'],
            223: ['FA', 'FA (Fractional Anisotropy)'],
            224: ['VR', 'VR (Volume Ratio)']
        }
        fig = plt.figure()
        plt.suptitle('Diffusion tensor biomarkers')

        for key, value in plot_dict.items():
            plt.subplot(key)
            plt.imshow(np.squeeze(self._biomarkers[value[0]]), cmap='gray')
            plt.axis('off')
            plt.title(value[1])

    #TODO
    def plot_FA_rgb(self):
        plot_dict = {
            111: ['FA_rgb', 'FA (Fractional Anisotropy)']
        }
        fig = plt.figure()
        plt.suptitle('Fractional Anisotropy Colormap')

        for key, value in plot_dict.items():
            plt.subplot(key)
            plt.imshow(np.squeeze(self._biomarkers[value[0]]))
            plt.axis('off')
            plt.title(value[1])

    """
    Weighted Least Squares
    """
    #TODO
    def _solve_wls(self, double[::1] pixel):
        cdef double[:, ::1] weights
        cdef double[::1] estimate

        weights = self._get_wls_weights(pixel)
        estimate = \
            np.matmul(
                np.linalg.pinv(
                    np.matmul(
                        np.matmul(
                            self._design_matrix.T, np.square(weights)
                        ), self._design_matrix
                    )
                ), np.matmul(
                        np.matmul(
                            (np.matmul(
                                weights, self._design_matrix
                            )).T, weights
                        ), np.log(pixel)
                    )
                )

        if np.isnan(np.sum(estimate)):
            estimate = np.zeros(np.shape(estimate))
        return estimate

    cdef double[:, ::1] _get_wls_weights(self, double[::1] pixel):
        """
        # TODO: implement other?
        In order of increasing WLS complexity: pixel < LLS estimate < Rice noise estimate
        :param pixel:
        :return:
        """
        cdef double[:, ::1] weights

        weights = np.multiply(np.eye(np.shape(pixel)[0]), pixel)
        return weights

    # TODO
    def _get_wls_error_value(self, double[::1] pixel, double[::1] wls_estimate):
        weights = self._get_wls_weights(pixel)
        wls_residual = weights @ (np.log(pixel) - self._design_matrix @ wls_estimate)
        wls_error = 1/2 * wls_residual.T @ wls_residual
        return wls_error

    # TODO
    def _get_wls_gradient(self, double[::1] pixel, double[::1] wls_estimate):
        cdef double[:, ::1] weights
        cdef double[:, ::1] J_matrix
        cdef double[::1] wls_gradient

        weights = self._get_wls_weights(pixel)

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(wls_estimate)
            wls_gradient = np.multiply((-1), J_matrix.T) @ self._design_matrix.T @ (weights.T @ weights) @ \
                           (np.log(pixel) - self._design_matrix @ wls_estimate)

        else:
            wls_gradient = np.multiply((-1), self._design_matrix.T) @ (weights.T @ weights) @ \
                           (np.log(pixel) - self._design_matrix @ wls_estimate)

        return wls_gradient

    # TODO
    def _get_wls_hessian(self, pixel, wls_estimate):
        weights = self._get_wls_weights(pixel)

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(wls_estimate)

            reduced_sum = np.zeros((7, 7))
            wls_residual = np.square(weights) @ (np.log(pixel) - self._design_matrix @ wls_estimate)
            for idx in range(np.shape(pixel)[0]):
                reduced_sum += np.multiply(wls_residual[idx, None], np.squeeze(self._P_matrix[:, :, idx]))

            wls_hessian = J_matrix.T @ self._design_matrix.T @ (weights.T @ weights) @ self._design_matrix @ \
                          J_matrix + reduced_sum

        else:
            wls_hessian = self._design_matrix.T @ (weights.T @ weights) @ self._design_matrix

        return wls_hessian

    """
    Nonlinear Least Squares
    """

    # TODO
    def _solve_nls(self, pixel):
        # Parameters
        lambda_param = 0
        hessian_flag = True

        # Initial solution
        estimate = self._solve_wls(pixel)
        error_best = self._get_error_value(pixel, estimate)

        # Iterate until convergence
        for k in range(self._max_iter):

            # Recalculate hessian if necessary
            if hessian_flag is True:
                gradient = self._get_gradient(pixel, estimate)
                hessian = self._get_hessian(pixel, estimate)
                hessian_flag = False

            # Check error for new parameter vector
            delta = np.multiply(
                (-1), np.linalg.pinv(hessian + np.multiply(lambda_param, self._lambda_matrix))
                ) @ gradient
            error_new = self._get_error_value(pixel, estimate+delta)

            # Check for convergence
            if abs(error_new - error_best) < self._error_epsilon \
                    and (0 <= (-1)*delta.T @ gradient < self._gradient_epsilon):
                if error_new < error_best:
                    estimate += delta
                break

            # Check if current estimate is better than previous
            if error_new < error_best:
                lambda_param *= 0.1
                estimate += delta
                hessian_flag = True
                error_best = error_new

            else:
                # Check if first iteration
                if lambda_param == 0:
                    lambda_param = 1e-4
                else:
                    lambda_param *= 10

        # Loop ended, get the final estimate
        if self._fix_method == 'cholesky':
            mfn_estimate = self._inverse_cholesky(estimate)
        else:
            mfn_estimate = estimate

        return mfn_estimate

    # TODO
    def _get_nls_error_value(self, pixel, nls_estimate):
        nls_residual = pixel - np.exp(self._design_matrix @ nls_estimate)
        nls_error = 1/2 * nls_residual.T @ nls_residual
        return nls_error

    # TODO
    def _get_nls_gradient(self, pixel, nls_estimate):
        pixel_estimated = np.exp(self._design_matrix @ nls_estimate)
        nls_residual = pixel - pixel_estimated
        pixel_estimated = np.eye(np.shape(pixel_estimated)[0]) * pixel_estimated[:, np.newaxis]

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(nls_estimate)
            nls_gradient = (-1) * J_matrix.T @ (pixel_estimated @ self._design_matrix).T @ nls_residual
        else:
            nls_gradient = (-1) * (pixel_estimated @ self._design_matrix).T @ nls_residual

        return nls_gradient

    # TODO
    def _get_nls_hessian(self, pixel, nls_estimate):
        pixel = np.eye(np.shape(pixel)[0]) * pixel[:, np.newaxis]
        pixel_estimated = np.exp(self._design_matrix @ nls_estimate)
        pixel_estimated = np.eye(np.shape(pixel_estimated)[0]) * pixel_estimated[:, np.newaxis]
        nls_residual = pixel - pixel_estimated

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(nls_estimate)

            reduced_sum = np.zeros((7, 7))
            coeff_diagonal = nls_residual @ pixel_estimated
            for idx in range(np.shape(pixel)[0]):
                reduced_sum += coeff_diagonal[idx, idx] * self._P_matrix[:, :, idx]

            nls_hessian = J_matrix.T @ self._design_matrix.T @ \
                          (pixel_estimated.T @ pixel_estimated - nls_residual @ pixel_estimated) \
                          @ self._design_matrix @ J_matrix + reduced_sum

        else:
            nls_hessian = self._design_matrix.T @ \
                          (pixel_estimated.T @ pixel_estimated - nls_residual @ pixel_estimated) \
                          @ self._design_matrix

        return nls_hessian

    """
    Cholesky parametrization
    """

    cdef double[:, ::1] _get_cholesky_J_matrix(self, double[::1] estimate):
        cdef double[:, ::1] J_matrix
        J_matrix = np.zeros((7, 7))

        J_matrix[:, 0] = array.array('d', [1, 0, 0, 0, 0, 0, 0])
        J_matrix[:, 1] = array.array('d', [0, 2 * estimate[1], 0, 0, estimate[4], 0, estimate[6]])
        J_matrix[:, 2] = array.array('d', [0, 0, 2 * estimate[2], 0, 0, estimate[5], 0])
        J_matrix[:, 3] = array.array('d', [0, 0, 0, 2 * estimate[3], 0, 0, 0])
        J_matrix[:, 4] = array.array('d', [0, 0, 2 * estimate[4], 0, estimate[1], estimate[6], 0])
        J_matrix[:, 5] = array.array('d', [0, 0, 0, 2 * estimate[5], 0, estimate[2], 0])
        J_matrix[:, 6] = array.array('d', [0, 0, 0, 2 * estimate[6], 0, estimate[4], estimate[1]])

        return J_matrix

    # TODO
    def _get_cholesky_P_matrix(self):
        W = self._design_matrix
        no_samples = np.shape(W)[0]
        P_matrix = np.zeros((7, 7, no_samples))

        for idx in range(no_samples):
            P_matrix[:, 0, idx] = [0, 0, 0, 0, 0, 0, 0]
            P_matrix[:, 1, idx] = [0, 2 * W[idx, 1], 0, 0, W[idx, 4], 0, W[idx, 6]]
            P_matrix[:, 2, idx] = [0, 0, 2 * W[idx, 2], 0, 0, W[idx, 5], 0]
            P_matrix[:, 3, idx] = [0, 0, 0, 2 * W[idx, 3], 0, 0, 0]
            P_matrix[:, 4, idx] = [0, W[idx, 4], 0, 0, 2 * W[idx, 2], 0, W[idx, 5]]
            P_matrix[:, 5, idx] = [0, 0, W[idx, 5], 0, 0, 2 * W[idx, 3], 0]
            P_matrix[:, 6, idx] = [0, W[idx, 6], 0, 0, W[idx, 5], 0, 2 * W[idx, 3]]

        self._P_matrix = (-1) * P_matrix

    # TODO
    def _inverse_cholesky(self, estimate):
        pixel_log = estimate[0]
        tensor_estimate = estimate[1:]

        Dxx = np.square(tensor_estimate[0])
        Dyy = np.square(tensor_estimate[1]) + np.square(tensor_estimate[3])
        Dzz = np.square(tensor_estimate[2]) + np.square(tensor_estimate[4]) + np.square(tensor_estimate[5])
        Dxy = tensor_estimate[0] * tensor_estimate[3]
        Dyz = tensor_estimate[1]*tensor_estimate[4] + tensor_estimate[3]*tensor_estimate[5]
        Dxz = tensor_estimate[0] * tensor_estimate[5]

        cholesky_estimate = [pixel_log, Dxx, Dyy, Dzz, Dxy, Dyz, Dxz]
        return cholesky_estimate


cdef dict run_pipeline(
        DWI dwi,
        str solver,
        str fix_method,
        bint plotting=0
    ):

    cdef DTISolver dti_solver
    cdef dict biomarkers

    dti_solver = DTISolver(dwi, solver, fix_method)
    dti_solver.estimate_tensor()
    dti_solver.estimate_eig()
    biomarkers = dti_solver.get_biomarkers()

    if plotting == 1:
        dti_solver.plot_tensor()
        dti_solver.plot_eig()
        dti_solver.plot_biomarkers()
        dti_solver.plot_FA_rgb()
        plt.show()

    return biomarkers


cpdef object run_module(object diffusion_data, str solver, str fix_method, bint plotting):
    # importing here avoids cyclic import problems
    from .mri_data import DiffusionData

    cdef DWI dwi

    if isinstance(diffusion_data, DiffusionData):

        if not hasattr(diffusion_data, 'mask'):
            diffusion_data = np.ones((np.shape(diffusion_data.data)[0], np.shape(diffusion_data)[1]))

        dwi = DWI(
            diffusion_data.data.copy(order='C'),
            diffusion_data.bvecs.copy(order='C'),
            diffusion_data.bvals.copy(order='C'),
            (diffusion_data.mask.copy(order='C')).astype(np.ushort)
        )

        diffusion_data.biomarkers = run_pipeline(dwi, solver, fix_method, plotting)
        return diffusion_data

    else:
        raise ValueError("Unexpected data format in module number 6!")
