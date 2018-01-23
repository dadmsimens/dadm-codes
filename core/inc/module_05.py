import numpy as np
import scipy.stats as st
import cmath
from . import simens_dadm as smns


def gk4(rsim):

    # function that prepares Gaussian window used to penalize pixels based on distance within window
    kerlen = 2 * rsim + 1
    nsig = 2
    interval = (2*nsig+1.)/kerlen
    x = np.linspace(-nsig-interval/2., nsig+interval/2., kerlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw/kernel_raw.sum()
    return kernel


def unlm(image, n_map):

    # setting window sizes to reduce number of parameters and chance failure caused by user
    rsearch = 5
    rsim = 2

    # get size for indexes
    [m, n] = image.shape

    # extend image at boundaries to make calculations on edges of image possible
    img_ext = np.pad(image, rsim, 'symmetric')

    # create penalty function
    penalty = np.asarray(gk4(rsim))

    # set space for filtered image
    output = np.zeros([m, n])

    # precompute possible window2
    window2_precomp = np.zeros((m, n, rsearch, rsearch))
    for i in range(2, m):
        for j in range(2, n):
            window2_precomp[i, j, :, :] = img_ext[i - rsim:i + rsim + 1, j - rsim:j + rsim + 1]

    # p pixel loop
    for i in range(0, m):
        for j in range(0, n):
            ii = i + rsim
            jj = j + rsim
            window1 = np.asarray(img_ext[ii - rsim:ii + rsim + 1, jj - rsim:jj + rsim + 1])

            # limit the search space
            pmin = max(ii - rsearch-1, rsim)
            pmax = min(ii + rsearch - 1, m)
            qmin = max(jj - rsearch-1, rsim)
            qmax = min(jj + rsearch - 1, n)

            # define placeholders for values
            w_max = 0
            avg = 0
            w_sum = 0

            # set exponential decay
            h_sq = 1 / np.square(1.22 * n_map[i, j])

            window2_slice = window2_precomp[pmin:pmax, qmin:qmax, :]
            window_diff = window1[None, None, :, :] - window2_slice
            d = np.sum(penalty[None, None, :, :] * (window_diff * window_diff), axis=(2, 3))

            w = np.exp((-1)*d * h_sq)

            # primitive way of handling case: pixel p == pixel q
            w[w == 1] = -100
            w_max = np.amax(w)
            w[w == -100] = w_max
            
            w_sum = np.sum(w, axis=(0, 1))
            avg = np.sum(w * img_ext[pmin:pmax, qmin:qmax], axis=(0, 1))

            avg = avg + w_max * img_ext[ii, jj]
            w_sum = w_sum + w_max

            if w_sum > 0:
                value = avg / w_sum
                output[i, j] = abs(cmath.sqrt(value * value - 2 * (np.square(n_map[i, j]))))
            else:
                output[i, j] = image[i, j]

    return output


def run_module(mri_input, other_arguments=None):

    if isinstance(mri_input, smns.mri_diff):
        [m, n, slices, grad] = mri_input.diffusion_data.shape
        data_out_diff = np.zeros([m, n, slices, grad])

        for i in range(slices):
            for j in range(grad):
                data_out_diff[:, :, i, j] = unlm(mri_input.diffusion_data[:, :, i, j], mri_input.diff_noise_map[:, :, i, j])

        mri_input.diffusion_data = data_out_diff

        [m, n, slices] = mri_input.structural_data.shape
        data_out_struct = np.zeros([m, n, slices])

        for i in range(slices):
            data_out_struct[:, :, i] = unlm(mri_input.structural_data[:, :, i], mri_input.struct_noise_map[:, :, i])

        mri_input.structural_data = data_out_struct

    elif isinstance(mri_input, smns.mri_struct):
        [m, n, slices] = mri_input.structural_data.shape
        data_out = np.zeros([m, n, slices])

        for i in range(slices):
            data_out[:, :, i] = unlm(mri_input.structural_data[:, :, i], mri_input.struct_noise_map[:, :, i])

        mri_input.structural_data = data_out

    else:
        return "Unexpected data format in module number 5!"

    return mri_input
