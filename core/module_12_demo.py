import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

import inc.module12 as m12
import inc.simens_dadm as smns

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_12_test/'

if __name__ == "__main__":

    data = sio.loadmat(DATASETS_ROOT + 'Imavol.mat')
    Imavol = data['Imavol']

    m12.main12(Imavol)
