import numpy as np
import math
from skimage.morphology import reconstruction, square, disk


def imimposemin(image, bw, conn=8):
    fm = image.copy().astype(np.float64)

    fm[bw == True] = -math.inf
    fm[bw == False] = math.inf

    if image.dtype == float:
        image_range = np.amax(image) - np.amin(image)

        if image_range == 0:
            h = 0.1
        else:
            h = image_range * 0.001
    else:
        h = 1

    fp1 = image + h

    g = np.minimum(fp1, fm)

    if conn == 8:
        selem = square(3)
    elif conn == 4:
        selem = disk(1)

    if image.dtype == float:
        J = reconstruction(1 - fm, 1 - g, selem=selem)
        J = 1 - J
    else:
        J = reconstruction(255 - fm, 255 - g, method='dilation', selem=selem)
        J = 255 - J
    J[bw] = 0

    return J