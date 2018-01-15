import numpy as np
import matplotlib.pyplot as plt


class DTISolver(object):

    MFN_MAX_ITER = 20
    MFN_ERROR_EPSILON = 1e-5
    MFN_GRADIENT_EPSILON = 1e-5
    MFN_LAMBDA_MATRIX_FUN = 'identity'

    def __init__(self, data, gradients, b_value, mask, solver, fix_method):

        self._data = data
        self._bvecs = gradients
        self._bvals = b_value
        self._mask = mask

        self._solver = solver
        self._fix_method = fix_method

        self._design_matrix = self._get_design_matrix()

        self._check_mask()
        self._setup_MFN()
        self._setup_solver()

    """
    Initialization
    """

    def _check_mask(self):
        if np.shape(self._mask)[0] == 0:
            self._mask = np.ones((self._data.shape[0], self._data.shape[1])) == 1

    def _get_design_matrix(self):
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
        # MFN method convergence breakpoints
        self._max_iter = DTISolver.MFN_MAX_ITER
        self._error_epsilon = DTISolver.MFN_ERROR_EPSILON
        self._gradient_epsilon = DTISolver.MFN_GRADIENT_EPSILON

        # Lambda parameter to multiply the hessian
        if DTISolver.MFN_LAMBDA_MATRIX_FUN == 'identity':
            self._lambda_matrix = np.eye(7)

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

    """
    Solvers
    """

    def _build_tensor(self, tensor_vector):
        tensor = np.zeros((3, 3))

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

    def _pixel_loop(self, image_depth, function_handle):

        output_image = np.zeros((np.shape(self._data)[0], np.shape(self._data)[1], image_depth))

        # very naive implementation
        for id_x in range(np.shape(self._data)[0]):
            for id_y in range(np.shape(self._data)[1]):

                if self._mask[id_x, id_y]:
                    output_image[id_x, id_y, :] = function_handle(self, id_x, id_y)

            if not np.floor(100*id_x/np.shape(self._data)[0]) % 10:
                print('Progress: {0:0.2f}%'.format(100*id_x/np.shape(self._data)[0]))

        return output_image

    def estimate_tensor(self):

        def estimate_tensor_pixel_func(DTISolver, id_x, id_y):
            pixel = np.squeeze(DTISolver._data[id_x, id_y, :])
            estimate = self._solver_func(pixel)
            return estimate[1:]

        self._tensor_image = self._pixel_loop(image_depth=6, function_handle=estimate_tensor_pixel_func)

    def estimate_eig(self):

        def estimate_eig_pixel_func(DTISolver, id_x, id_y):
            tensor = self._build_tensor(np.squeeze(DTISolver._tensor_image[id_x, id_y, :]))
            eig_vals, eig_vectors = np.linalg.eigh(tensor)

            # eigenvalues in ascending order, flip array
            eig_vals = eig_vals[::-1]

            # get RGB values (from eigenvectr corresponding to largest eigenvalue)
            # red: transversal (left-right)
            # green: anterior-posterior (front-back)
            # blue: cranio-caudal (head-feet)
            # we take absolute value because we care about the axis in general, not direction specifically
            rgb = np.abs(eig_vectors[:, -1])

            if self._fix_method == 'abs':
                eig_vals = np.abs(eig_vals)

            return np.hstack((eig_vals, rgb))

        results = self._pixel_loop(image_depth=6, function_handle=estimate_eig_pixel_func)

        # split results into eigenvalues and rgb map
        self._eig_image = results[:, :, 0:3]
        self._rgb_image = results[:, :, 3:]

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
    def _solve_wls(self, pixel):
        weights = self._get_wls_weights(pixel)
        estimate = np.linalg.pinv(self._design_matrix.T @ np.square(weights) @ self._design_matrix) @ \
                   (weights @ self._design_matrix).T @ weights @ np.log(pixel)

        if np.isnan(np.sum(estimate)):
            estimate = np.zeros(np.shape(estimate))
        return estimate

    def _get_wls_weights(self, pixel):
        """
        In order of increasing WLS complexity: pixel < LLS estimate < Rice noise estimate
        :param pixel:
        :return:
        """
        # TODO: implement others
        weights = np.eye(np.shape(pixel)[0]) * pixel[:, np.newaxis]
        return weights

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


def run_pipeline(dwi, solver, fix_method, plotting=False):

    # convert data for compatibility with CORE
    structural_data = dwi.structural_data
    diffusion_data = dwi.diffusion_data
    data = np.concatenate((structural_data, diffusion_data), axis=2)

    b_value = np.concatenate((np.zeros((np.shape(structural_data)[2])), dwi.b_value), axis=0)
    gradients = np.concatenate((np.zeros((np.shape(structural_data)[2], 3)), dwi.gradients), axis=0)

    # only one slice
    data = np.squeeze(data)

    dti_solver = DTISolver(
        data=data,
        gradients=gradients,
        b_value=b_value,
        mask=dwi.skull_stripping_mask,
        solver=solver,
        fix_method=fix_method
    )
    dti_solver.estimate_tensor()
    dti_solver.estimate_eig()
    biomarkers = dti_solver.get_biomarkers()

    if plotting is True:
        dti_solver.plot_tensor()
        dti_solver.plot_eig()
        dti_solver.plot_biomarkers()
        dti_solver.plot_FA_rgb()
        plt.show()

    return biomarkers


def run_module(mri_diff, solver, fix_method, plotting=False):
    # importing here avoids cyclic import problems
    from . import simens_dadm as smns

    if isinstance(mri_diff, smns.mri_diff):
        mri_diff.biomarkers = run_pipeline(mri_diff, solver, fix_method, plotting)
        return mri_diff

    else:
        raise ValueError("Unexpected data format in module number 6!")
