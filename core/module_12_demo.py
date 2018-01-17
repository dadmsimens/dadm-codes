import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import inc.module12 as module12
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATASETS_ROOT = PROJECT_ROOT + '/Data/Module_12_test/'

if __name__ == "__main__":

    data = sio.loadmat(DATASETS_ROOT + 'Imavol.mat')

    Imavol = data['Imavol']

    [X,Y,Z] = module12.transrotateplane(Imavol, -45, 0, 45, 0)

    plt3d = plt.figure().gca(projection='3d', azim=250)
    plt3d.plot_surface(X, Y, Z)
    plt.show()

    image = module12.interpolatemri(Imavol, X, Y, Z)
    imgplot = plt.imshow(image,cmap='gray')
    plt.show()