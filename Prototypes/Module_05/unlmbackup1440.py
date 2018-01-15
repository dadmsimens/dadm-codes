from create_penalty import create_penalty, gauss_kernel, gk
import numpy as np
import math
import cmath


def unlm(image, rsearch, rsim, n_map):
    # get size for indexes
    [m, n] = image.shape

    # extend image at boundaries to make calculations on edges of image possible
    img_ext = np.pad(image, rsim, 'symmetric')

    # create penalty function
    penalty = np.asarray(gk(rsim))

    # set space for filtered image
    output = np.zeros([m, n])

    # p pixel loop
    for i in range(0, m):
        for j in range(0, n):
            ii = i + rsim
            jj = j + rsim
            window_1 = np.asarray(img_ext[ii - rsim:ii + rsim + 1, jj - rsim:jj + rsim + 1])

            # limit the search space
            pmin = max(ii - rsearch-1, rsim)
            pmax = min(ii + rsearch-1, m + rsim-1)
            qmin = max(jj - rsearch-1, rsim)
            qmax = min(jj + rsearch-1, n + rsim-1)

            # define placeholders for values
            w_max = 0
            avg = 0
            w_sum = 0

            # loop within search space
            for p in range(pmin, pmax + 1):
                for q in range(qmin, qmax + 1):
                    if p == ii and q == jj:
                        continue  # leave central pixel (case p=q)

                    # TODO: vectorize
                    window_2 = np.asarray(img_ext[p - rsim:p + rsim + 1, q - rsim:q + rsim + 1])

                    # calculate distance
                    # TODO: vectorize
                    d = np.sum(np.sum(penalty * np.square(window_1 - window_2)))
                    #d=1

                    # set exponential decay, 1.22 is optimal according to article
                    h = 1.22 * n_map[i, j]

                    w = np.exp(-d / (h*h))

                    if w > w_max:
                        w_max = w

                    w_sum = w_sum + w
                    avg = avg + w * img_ext[p, q]

            avg = avg + w_max * img_ext[ii, jj]
            w_sum = w_sum + w_max

            if w_sum > 0:
                value = avg / w_sum
                output[i, j] = abs(cmath.sqrt(value * value - 2 * (np.square(n_map[i, j]))))
            else:
                output[i, j] = image[i, j]

    return output
