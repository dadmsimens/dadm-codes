import numpy as np


def strel(type, size):
    a, b = size, size
    n = 2 * size + 1
    if type == 'disk':
        y, x = np.ogrid[-a:n-a, -b:n-b]
        mask = x*x + y*y <= size*size
        array = np.ones((size * 2 + 1, size * 2 + 1))
        array[mask] = 0
    if type == 'array':
        mask = np.ones((a, b), dtype=bool)
        array = np.ones((a, b))
        array[mask] = 0
    return array
