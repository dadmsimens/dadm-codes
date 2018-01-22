import numpy as np
import matplotlib.pyplot as plt


class DTISolver(object):

    MFN_MAX_ITER = 20
    MFN_ERROR_EPSILON = 1e-5
    MFN_GRADIENT_EPSILON = 1e-5
    MFN_LAMBDA_MATRIX_FUN = 'identity'
    MFN_LAMBDA_PARAM_INIT = 1e-4

    ACCEPTED_SOLVERS = ['wls', 'nls']
    ACCEPTED_FIX_METHODS = ['abs', 'cholesky']

    def __init__(self, data, gradients, b_value, mask, solver, fix_method, mute_progress=True):

        self._data = data
        self._bvecs = gradients
        self._bvals = b_value
        self._mask = mask

        self._solver = solver
        self._fix_method = fix_method
        self._mute_progress = mute_progress

        self._check_input()
        self._check_mask()
        self._check_solver()

        self._design_matrix = self._get_design_matrix()

        self._setup_MFN()
        self._setup_solver()

        # Attributes assigned during pipeline execution
        self._tensor_image = None
        self._eig_image = None
        self._rgb_image = None
        self._biomarkers = None

    """
    Initialization
    """

    def _check_input(self):
        data_dims = np.shape(self._data)
        bvecs_dims = np.shape(self._bvecs)
        bvals_dims = np.shape(self._bvals)

        if (
            len(data_dims) != 3 or
            len(bvecs_dims) != 2 or
            len(bvals_dims) != 1 or
            bvecs_dims[1] != 3 or
            bvecs_dims[0] != bvals_dims[0] or
            bvals_dims[0] != data_dims[2]
        ):
            raise ValueError('Incompatible shapes of input data (mri_data, gradients, b_value).')

        if np.amin(self._data) <= 0:
            raise ValueError('Voxel value cannot be negative.')

    def _check_mask(self):
        if np.shape(self._mask)[0] == 0 or not np.array_equal(self._mask, self._mask.astype(bool)) or \
                (np.shape(self._mask)[0] != np.shape(self._data)[0]
                 and (np.shape(self._mask)[1] != np.shape(self._data)[1])):
            self._mask = np.ones((self._data.shape[0], self._data.shape[1])) == 1

    def _get_design_matrix(self):
        # TODO: change shape to (1, 1, gradient, 7)?
        design_matrix = np.column_stack((
            np.square(self._bvecs[:, 0]),
            np.square(self._bvecs[:, 1]),
            np.square(self._bvecs[:, 2]),
            2 * np.multiply(self._bvecs[:, 0], self._bvecs[:, 1]),
            2 * np.multiply(self._bvecs[:, 1], self._bvecs[:, 2]),
            2 * np.multiply(self._bvecs[:, 0], self._bvecs[:, 2])
        ))
        design_matrix *= (-1)*self._bvals[:, np.newaxis]
        design_matrix = np.insert(design_matrix, 0, np.ones(self._bvals.shape), axis=1)

        return design_matrix

    def _setup_MFN(self):
        dims = np.shape(self._data)
        # MFN method convergence breakpoints
        self._max_iter = DTISolver.MFN_MAX_ITER
        self._error_epsilon = DTISolver.MFN_ERROR_EPSILON * np.ones((dims[0], dims[1]))
        self._gradient_epsilon = DTISolver.MFN_GRADIENT_EPSILON * np.ones((dims[0], dims[1]))
        self._lambda_param_init = DTISolver.MFN_LAMBDA_PARAM_INIT

        # Lambda parameter to multiply the hessian
        if DTISolver.MFN_LAMBDA_MATRIX_FUN == 'identity':
            self._lambda_matrix = self._last_dim_to_eye(np.ones((dims[0], dims[1], 7,)))

        if self._fix_method == 'cholesky':
            self._get_cholesky_P_matrix()

    def _setup_solver(self):
        if self._solver == 'wls':
            self._solver_func = self._solve_wls
            self._get_error_value = self._get_wls_error_value
            self._get_gradient = self._get_wls_gradient
            self._get_hessian = self._get_wls_hessian

            if self._fix_method == 'cholesky':
                self._solver_func = self._solve_nls

        elif self._solver == 'nls':
            self._solver_func = self._solve_nls
            self._get_error_value = self._get_nls_error_value
            self._get_gradient = self._get_nls_gradient
            self._get_hessian = self._get_nls_hessian

        else:
            raise ValueError('Invalid DTI SOLVER type.')

    def _check_solver(self):
        if self._solver not in self.ACCEPTED_SOLVERS:
            raise ValueError('Invalid DTI SOLVER type.')
        if self._fix_method not in self.ACCEPTED_FIX_METHODS:
            raise ValueError('Invalid DTI FIX_METHOD type.')

    """
    Solvers
    """

    def _reshape_tensor_image(self):
        dims = np.shape(self._tensor_image)
        tensor_image_reshaped = np.zeros((dims[0], dims[1], 3, 3))

        # x-row
        tensor_image_reshaped[:, :, 0, 0] = self._tensor_image[:, :, 0]
        tensor_image_reshaped[:, :, 0, 1] = self._tensor_image[:, :, 3]
        tensor_image_reshaped[:, :, 0, 2] = self._tensor_image[:, :, 5]

        # y-row
        tensor_image_reshaped[:, :, 1, 0] = self._tensor_image[:, :, 3]
        tensor_image_reshaped[:, :, 1, 1] = self._tensor_image[:, :, 1]
        tensor_image_reshaped[:, :, 1, 2] = self._tensor_image[:, :, 4]

        # z-row
        tensor_image_reshaped[:, :, 2, 0] = self._tensor_image[:, :, 5]
        tensor_image_reshaped[:, :, 2, 1] = self._tensor_image[:, :, 4]
        tensor_image_reshaped[:, :, 2, 2] = self._tensor_image[:, :, 2]

        return tensor_image_reshaped

    def estimate_tensor(self):

        dims = np.shape(self._data)
        self._tensor_image = np.where(self._mask[:, :, None], self._solver_func(), np.zeros((dims[0], dims[1], 7)))

        # First value in each voxel is an estimate of ln(pixel_measurement); thus ignore
        self._tensor_image = self._tensor_image[:, :, 1:]

    def estimate_eig(self):

        tensor_image_reshaped = self._reshape_tensor_image()

        dims = np.shape(self._tensor_image)
        eig_values, eig_vectors = np.linalg.eigh(tensor_image_reshaped)
        eig_values = np.where(self._mask[:, :, None], eig_values, np.zeros((dims[0], dims[0], 3)))
        eig_vectors = np.where(self._mask[:, :, None, None], eig_vectors, np.zeros((dims[0], dims[0], 3, 3)))

        # eigenvalues in ascending order, flip array
        self._eig_image = np.flip(eig_values, axis=2)

        # get RGB values (from eienvector corresponding to largest eigenvalue)
        # red: transversal (left-right)
        # green: anterior-posterior (front-back)
        # blue: cranio-caudal (head-feet)
        # we take absolute value because we care about the axis in general, not direction specifically
        self._rgb_image = np.abs(eig_vectors[:, :, :, -1])

        if self._fix_method == 'abs':
            self._eig_image = np.abs(self._eig_image)

    """
    Biomarkers
    """

    def get_biomarkers(self):
        MD = self._get_marker_MD()
        RA = self._get_marker_RA()
        FA = self._get_marker_FA()
        VR = self._get_marker_VR()
        FA_rgb = FA[:, :, np.newaxis] * self._rgb_image

        biomarkers = {
            'MD': MD,
            'RA': RA,
            'FA': FA,
            'VR': VR,
            'FA_rgb': FA_rgb
        }

        self._biomarkers = biomarkers
        return biomarkers

    def _get_marker_MD(self):
        return np.mean(self._eig_image, axis=2)

    def _get_marker_RA(self):
        MD = self._get_marker_MD()
        eig_variance = self._get_eig_variance()

        RA = np.zeros(np.shape(MD))
        RA[self._mask] = np.sqrt(np.divide(eig_variance[self._mask], 3*MD[self._mask]))
        return RA

    def _get_marker_FA(self):
        eig_variance = self._get_eig_variance()
        sum_squares = np.sum(np.square(self._eig_image), axis=2)

        FA = np.zeros(np.shape(eig_variance))
        FA[self._mask] = np.sqrt(3/2) * \
                             np.sqrt(np.divide(eig_variance[self._mask], sum_squares[self._mask]))
        return FA

    def _get_marker_VR(self):
        MD = self._get_marker_MD()

        VR = np.zeros(np.shape(MD))
        VR[self._mask] = np.divide(
            (np.prod(self._eig_image, axis=2))[self._mask], np.power(MD[self._mask], 3)
        )
        return VR

    def _get_eig_variance(self):
        MD = self._get_marker_MD()
        return np.sum(np.square(self._eig_image - MD[:, :, np.newaxis]), axis=2)

    """
    Plotting (debug)
    """

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

    def _solve_wls(self):

        weights = self._get_wls_weights()
        estimate = np.matmul(
            np.matmul(
                self._design_matrix.T[None, None, :, :],
                np.square(weights)
            ),
            self._design_matrix[None, None, :, :]
        )
        estimate = np.matmul(
            np.linalg.inv(estimate),
            np.transpose(
                np.matmul(
                    weights,
                    self._design_matrix[None, None, :, :]
                ), axes=(0, 1, 3, 2))
        )
        estimate = np.matmul(
            np.matmul(
                estimate,
                weights
            ),
            np.log(self._data)[:, :, :, None]
        )
        estimate = np.squeeze(estimate)

        # check for NaNs and convert them to zeros
        estimate_isnan = np.isnan(estimate)
        if np.amax(estimate_isnan) == True:
            estimate = np.where(estimate_isnan, 0, estimate)

        return estimate

    def _get_wls_weights(self):
        """
        Chosen WLS Model: weights equal to measurement in each pixel.

        Other models, in order of increasing complexity:
        pixel < LLS estimate < Rice noise estimate
        """
        # Chosen WLS Model: weights equal to measurement in each pixel
        return self._last_dim_to_eye(self._data)

    def _get_wls_error_value(self, pixel, wls_estimate):
        weights = self._get_wls_weights(pixel)
        wls_residual = weights @ (np.log(pixel) - self._design_matrix @ wls_estimate)
        wls_error = 1/2 * wls_residual.T @ wls_residual
        return wls_error

    def _get_wls_gradient(self, pixel, wls_estimate):
        weights = self._get_wls_weights(pixel)

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(wls_estimate)
            wls_gradient = (-1) * J_matrix.T @ self._design_matrix.T @ (weights.T @ weights) @ \
                           (np.log(pixel) - self._design_matrix @ wls_estimate)

        else:
            wls_gradient = (-1) * self._design_matrix.T @ (weights.T @ weights) @ \
                           (np.log(pixel) - self._design_matrix @ wls_estimate)

        return wls_gradient

    def _get_wls_hessian(self, pixel, wls_estimate):
        weights = self._get_wls_weights(pixel)

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(wls_estimate)

            reduced_sum = np.zeros((7, 7))
            wls_residual = np.square(weights) @ (np.log(pixel) - self._design_matrix @ wls_estimate)
            for idx in range(np.shape(pixel)[0]):
                reduced_sum += wls_residual[idx, np.newaxis] * np.squeeze(self._P_matrix[:, :, idx])

            wls_hessian = J_matrix.T @ self._design_matrix.T @ (weights.T @ weights) @ self._design_matrix @ \
                          J_matrix + reduced_sum

        else:
            wls_hessian = self._design_matrix.T @ (weights.T @ weights) @ self._design_matrix

        return wls_hessian

    """
    Nonlinear Least Squares
    """

    '''
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
            delta = (-1) * np.linalg.pinv(hessian + lambda_param*self._lambda_matrix) @ gradient
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
    '''
    def _solve_nls(self):
        dims = np.shape(self._data)

        # Parameters
        lambda_param = self._lambda_matrix * self._lambda_param_init
        hessian_flag = np.ones((dims[0], dims[1])) == 1
        numerical_zero_epsilon = self._lambda_matrix * 1e-8

        # Initial solution
        estimate = np.where(self._mask[:, :, None], self._solve_wls(), np.zeros((dims[0], dims[1], 7)))
        error_best = self._get_error_value(estimate)

        # Boolean array of pixels for calculation (skull mask, convergence check)
        pixel_mask = self._mask

        # Initial values
        gradient = np.zeros((dims[0], dims[1], 7))
        hessian = np.zeros((dims[0], dims[1], 7, 7))
        delta = np.zeros((np.shape(estimate)))
        gradient_check = np.zeros((np.shape(self._gradient_epsilon)))

        # Iterate until convergence
        for k in range(self._max_iter):

            # Recalculate hessian and gradient if necessary
            gradient = np.where((pixel_mask*hessian_flag)[:, :, None], self._get_gradient(estimate), gradient)
            hessian = np.where((pixel_mask*hessian_flag)[:, :, None, None], self._get_hessian(estimate), hessian)
            hessian_flag = np.where(pixel_mask*hessian_flag, False, hessian_flag)

            # Check error for new parameter vector
            delta = np.where(
                pixel_mask[:, :, None],
                (-1) * np.squeeze(
                        np.matmul(
                            np.linalg.inv(hessian + lambda_param*self._lambda_matrix + numerical_zero_epsilon),
                            gradient[:, :, :, None]
                        )
                    ),
                delta
            )
            error_new = np.where(pixel_mask, self._get_error_value(estimate+delta), error_best)

            # Check for convergence
            gradient_check = np.where(
                pixel_mask,
                np.squeeze(
                        np.matmul(
                            np.transpose(delta[:, :, :, None], axes=(0, 1, 3, 2)),
                            gradient[:, :, :, None]
                        )
                    ),
                gradient_check
            )
            check_convergence = abs(error_new - error_best) < self._error_epsilon
            check_convergence *= 0 <= gradient_check
            check_convergence *= gradient_check < self._gradient_epsilon

            # Update final estimate only for voxels that converged this iteration AND are valid (pixel mask)
            estimate = np.where((check_convergence*pixel_mask)[:, :, None], estimate+delta, estimate)

            # Check if current estimate is better than previous
            check_lower_error = (error_new < error_best) * pixel_mask

            lambda_param = np.where(check_lower_error[:, :, None, None], lambda_param*0.1, lambda_param*10)
            estimate = np.where(check_lower_error[:, :, None], estimate+delta, estimate)
            error_best = np.where(check_lower_error, error_new, error_best)
            hessian_flag = np.where(check_lower_error, True, hessian_flag)

            # Update pixel mask
            pixel_mask = np.where(check_convergence, False, pixel_mask)
            if np.amax(pixel_mask) == False:
                break

        # Loop ended, get the final estimate
        if self._fix_method == 'cholesky':
            mfn_estimate = self._inverse_cholesky(estimate)
        else:
            mfn_estimate = estimate

        return mfn_estimate

    def _get_nls_error_value(self, nls_estimate):
        nls_residual = self._data - np.squeeze(
            np.exp(np.matmul(self._design_matrix[None, None, :, :], nls_estimate[:, :, :, None]))
        )
        nls_error = 1 / 2 * np.sum(np.square(nls_residual), axis=2)
        return nls_error

    def _get_nls_gradient(self, nls_estimate):
        pixel_estimated = np.squeeze(
            np.exp(np.matmul(self._design_matrix[None, None, :, :], nls_estimate[:, :, :, None]))
        )
        nls_residual = self._data - pixel_estimated
        pixel_estimated = self._last_dim_to_eye(pixel_estimated)

        if self._fix_method == 'cholesky':
            J_matrix = self._get_cholesky_J_matrix(nls_estimate)
            nls_gradient = (-1) * J_matrix.T @ (pixel_estimated @ self._design_matrix).T @ nls_residual
        else:
            nls_gradient = (-1) * np.matmul(
                np.transpose(
                    np.matmul(pixel_estimated, self._design_matrix[None, None, :, :]), axes=(0, 1, 3, 2)
                ),
                nls_residual[:, :, :, None]
            )

        return np.squeeze(nls_gradient)

    def _get_nls_hessian(self, nls_estimate):
        pixel = self._last_dim_to_eye(self._data)
        pixel_estimated = np.squeeze(
            np.exp(np.matmul(self._design_matrix[None, None, :, :], nls_estimate[:, :, :, None]))
        )
        pixel_estimated = self._last_dim_to_eye(pixel_estimated)
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
            nls_hessian = np.matmul(
                np.matmul(
                    self._design_matrix.T [None, None, :, :],
                    (np.square(pixel_estimated) - np.matmul(nls_residual, pixel_estimated))
                ),
                self._design_matrix[None, None, :, :]
            )

        return nls_hessian

    '''
    def _get_nls_error_value(self, pixel, nls_estimate):
        nls_residual = pixel - np.exp(self._design_matrix @ nls_estimate)
        nls_error = 1/2 * nls_residual.T @ nls_residual
        return nls_error

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
    '''

    """
    Cholesky parametrization
    """

    def _get_cholesky_J_matrix(self, estimate):
        J_matrix = np.zeros((7, 7))

        J_matrix[:, 0] = [1, 0, 0, 0, 0, 0, 0]
        J_matrix[:, 1] = [0, 2 * estimate[1], 0, 0, estimate[4], 0, estimate[6]]
        J_matrix[:, 2] = [0, 0, 2 * estimate[2], 0, 0, estimate[5], 0]
        J_matrix[:, 3] = [0, 0, 0, 2 * estimate[3], 0, 0, 0]
        J_matrix[:, 4] = [0, 0, 2 * estimate[4], 0, estimate[1], estimate[6], 0]
        J_matrix[:, 5] = [0, 0, 0, 2 * estimate[5], 0, estimate[2], 0]
        J_matrix[:, 6] = [0, 0, 0, 2 * estimate[6], 0, estimate[4], estimate[1]]

        return J_matrix

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

    """
    Other methods
    """

    @staticmethod
    def _last_dim_to_eye(input_array):
        dims = np.shape(input_array)
        eye_matrix = np.eye(dims[2])
        eye_matrix = np.expand_dims(eye_matrix, axis=0)
        eye_matrix = np.expand_dims(eye_matrix, axis=0)
        reshaped_input = eye_matrix * input_array[:, :, :, np.newaxis]
        return reshaped_input


def _prepare_data(dwi):

    structural_data = dwi.structural_data
    diffusion_data = dwi.diffusion_data
    if len(np.shape(structural_data)) < 4:
        # add dummy diffusion direction
        structural_data = np.expand_dims(structural_data, axis=3)

    data_mri = np.concatenate((structural_data, diffusion_data), axis=3)

    if np.shape(dwi.b_value)[0] == 1:
        b_value = np.repeat(dwi.b_value, repeats=np.shape(diffusion_data)[3])
    else:
        b_value = dwi.b_value

    b_value = np.concatenate((np.zeros((np.shape(structural_data)[3])), b_value), axis=0)
    gradients = np.concatenate((np.zeros((np.shape(structural_data)[3], 3)), dwi.gradients), axis=0)

    return data_mri, b_value, gradients


def run_pipeline(dwi, solver, fix_method, plotting=False, mute_progress=True):

    data_mri, b_value, gradients = _prepare_data(dwi)

    num_slices = np.shape(data_mri)[2]
    biomarkers = []

    for slice_idx in range(num_slices):
        print('Computing DTI on slice {} out of {}...'.format(slice_idx, num_slices))
        # only one slice
        data = np.squeeze(data_mri[:, :, slice_idx, :])

        try:
            mask = np.squeeze(dwi.skull_stripping_mask[:, :, slice_idx])
        except:
            # if mask is not defined for given slice
            mask = []

        dti_solver = DTISolver(
            data=data,
            gradients=gradients,
            b_value=b_value,
            mask=mask,
            solver=solver,
            fix_method=fix_method,
            mute_progress=mute_progress
        )
        dti_solver.estimate_tensor()
        dti_solver.estimate_eig()
        biomarkers.append(dti_solver.get_biomarkers())

        if plotting is True:
            dti_solver.plot_tensor()
            dti_solver.plot_eig()
            dti_solver.plot_biomarkers()
            dti_solver.plot_FA_rgb()
            plt.show()

    print("DTI done.")
    return biomarkers


def run_module(mri_diff, solver, fix_method, plotting=False, mute_progress=True):
    # importing here avoids cyclic import problems
    from . import simens_dadm as smns

    if isinstance(mri_diff, smns.mri_diff):
        mri_diff.biomarkers = run_pipeline(mri_diff, solver, fix_method, plotting, mute_progress)
        return mri_diff

    else:
        raise ValueError("Expected MRI_DIFF object instance, received unknown type.")
