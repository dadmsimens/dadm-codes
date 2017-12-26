
import numpy as np


class DTISolver:

    MFN_MAX_ITER = 20
    MFN_NLS_EPSILON = 1e-5
    MFN_GRADIENT_EPSILON = 1e-5
    MFN_LAMBDA_MATRIX_FUN = 'identity'

    def __init__(self, dwi, solver, fix_method):

        self._dwi = dwi
        self._solver = solver
        self._fix_method = fix_method

        self._design_matrix = self._get_design_matrix()

        self._setup_MFN()
        self._setup_solver()

    def _get_design_matrix(self):
        design_matrix = np.column_stack((
            np.square(self._dwi.bvecs[:, 0]),
            np.square(self._dwi.bvecs[:, 1]),
            np.square(self._dwi.bvecs[:, 2]),
            2 * np.multiply(self._dwi.bvecs[:, 0], self._dwi.bvecs[:, 1]),
            2 * np.multiply(self._dwi.bvecs[:, 1], self._dwi.bvecs[:, 2]),
            2 * np.multiply(self._dwi.bvecs[:, 0], self._dwi.bvecs[:, 2])
        ))
        design_matrix *= (-1)*self._dwi.bvals[:, np.newaxis]
        design_matrix = np.insert(design_matrix, 0, np.ones(self._dwi.bvals.shape), axis=1)

        return design_matrix

    def _setup_MFN(self):
        # MFN method convergence breakpoints
        self._max_iter = DTISolver.MFN_MAX_ITER
        self._nls_epsilon = DTISolver.MFN_NLS_EPSILON
        self._gradient_epsilon = DTISolver.MFN_GRADIENT_EPSILON

        # Lambda parameter to multiply the hessian
        if 'identity' == DTISolver.MFN_LAMBDA_MATRIX_FUN:
            self._lambda_matrix = np.eye(7)

    def _setup_solver(self):
        if self._solver == 'wls':
            self._solver_func = self._solve_wls
            self._get_error_value = self._get_wls_error_value
            self._get_gradient = self._get_wls_gradient
            self._get_hessian = self._get_wls_hessian

        elif self._solver == 'nls':
            self._solver_func = self._solve_nls

        else:
            raise ValueError('Invalid DTI SOLVER type.')

    def solve(self):
        tensor_image = np.zeros((np.shape(self._dwi.data)[0], np.shape(self._dwi.data)[1], 6))

        # very naive implementation
        for id_x in range(np.shape(self._dwi.data)[0]):
            for id_y in range(np.shape(self._dwi.data)[1]):
                if self._dwi.mask[id_x, id_y] is not 0:
                    pixel = np.squeeze(self._dwi.data[id_x, id_y, :])
                    estimate = self._solver_func(pixel)
                    tensor_image[id_x, id_y, :] = estimate[1:]

            print('Progress: {0:0.2f}%'.format(100*id_x/np.shape(self._dwi.data)[0]))

        return tensor_image

    """
    Weighted Least Squares implementation
    """
    def _solve_wls(self, pixel):
        weights = self._get_wls_weights(pixel)
        weights = np.eye(np.shape(weights)[0]) * weights[:, np.newaxis]
        estimate = np.linalg.pinv(self._design_matrix.T @ np.square(weights) @ self._design_matrix) @ \
                   (weights @ self._design_matrix).T @ weights @ np.log(pixel)
        return estimate

    def _get_wls_weights(self, pixel):
        """
        In order of increasing WLS complexity: pixel < LLS estimate < Rice noise estimate
        :param pixel:
        :return:
        """
        # TODO: implement others
        return pixel

    def _get_wls_error_value(self, wls_estimate):
        weights = self._get_wls_weights(wls_estimate)
        pixel_estimated = weights[:, np.newaxis] * (np.log(wls_estimate) - self._design_matrix @ wls_estimate)
        wls_error = 1/2 * pixel_estimated.T @ wls_estimate
        return wls_error

    def _get_wls_gradient(self, wls_estimate):
        weights = self._get_wls_weights(wls_estimate)

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(wls_estimate)
            wls_gradient = (-1) * J_matrix.T @ self._design_matrix.T @ (weights @ weights.T) @ \
                           (np.log(wls_estimate) - self._design_matrix @ wls_estimate)

        else:
            wls_gradient = (-1) * self._design_matrix.T @ (weights @ weights.T) @ \
                           (np.log(wls_estimate) - self._design_matrix @ wls_estimate)

        return wls_gradient

    def _get_wls_hessian(self):
        pass

    """
    Nonlinear Least Squares implementation
    """

    def _solve_nls(self, pixel):
        # Parameters
        lambda_param = 0
        hessian_flag = 1

    """
    Cholesky parametrization implementation
    """

    def _get_cholesky_J_matrix(self, estimate):
        J_matrix = np.zeros((7, 7))

        J_matrix[:, 0] = [1, 0, 0, 0, 0, 0, 0]
        J_matrix[:, 1] = [0, 2 * estimate(1), 0, 0, estimate(4), 0, estimate(6)]
        J_matrix[:, 2] = [0, 0, 2 * estimate(2), 0, 0, estimate(5), 0]
        J_matrix[:, 3] = [0, 0, 0, 2 * estimate(3), 0, 0, 0]
        J_matrix[:, 4] = [0, 0, 2 * estimate(4), 0, estimate(1), estimate(6), 0]
        J_matrix[:, 5] = [0, 0, 0, 2 * estimate(5), 0, estimate(2), 0]
        J_matrix[:, 6] = [0, 0, 0, 2 * estimate(6), 0, estimate(4), estimate(1)]

        return J_matrix
