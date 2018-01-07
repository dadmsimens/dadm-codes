# only changing matlab prototype to python without good structure
# very sketchy prototype but now it's working quite good
# TO_DO remove small holes in mask

import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.io import loadmat
import numpy as np
from strel import strel
from imimposemin import imimposemin
# MUST TO CHANGE
from skimage import morphology


class SkullStriping:
    def __init__(self, filename):
        self.filename = filename

    def strip(self):

        result = None

        mat_dict = loadmat(self.filename)
        image = mat_dict['SENSE_Tikhonov']
        fig = plt.figure()
        plt.gray()  # show the filtered result in grayscale
        ax1 = fig.add_subplot(121)  # left side
        ax2 = fig.add_subplot(122)  # right side
        sx = ndimage.sobel(image, axis=0, mode='constant')
        sy = ndimage.sobel(image, axis=1, mode='constant')
        gradmag = np.hypot(sx, sy)
        se = strel('disk', 20)
        i_open = ndimage.morphology.grey_opening(image, 20)
        i_erode = ndimage.morphology.grey_erosion(image, 20)
        #TO_DO grey_reconstruction
        i_obr = morphology.reconstruction(i_erode, image)
        i_obrd = ndimage.grey_dilation(i_obr, 20)
        i_complement = 1 - i_erode
        i_obrcbr = morphology.reconstruction((1-i_obrd), (1-i_obr))
        i_obrcbr = 1 - i_obrcbr
        #regionmax
        neighborhood = ndimage.generate_binary_structure(2, 2)
        fgm = ndimage.maximum_filter(i_obrcbr, footprint=neighborhood)
        #se2 = strel('array', 5)
        fgm2 = ndimage.morphology.grey_closing(fgm, 5)
        fgm3 = ndimage.morphology.grey_erosion(fgm2, 5)
        #is it the same?
        fgm4 = ndimage.morphology.grey_opening(fgm3, 20)
        log = fgm4 >= 80
        i3 = image
        #print(image)
        #i3(fgm4) = 255
        #i_recon = ndimage.binary_propagation(i_erode, image)


        threshold, upper, lower = 100, 1, 0
        bw = np.where(image > threshold, upper, lower)
        d = ndimage.morphology.distance_transform_edt(bw)
        markers = ndimage.label(bw)[0]
        dL = ndimage.watershed_ift(d.astype(np.uint8), markers)
        bgm = dL == 1
        bgm = np.invert(bgm)

        gradmag2 = imimposemin(gradmag, bgm | log)

        markers = ndimage.label(gradmag2)[0]
        L = ndimage.watershed_ift(gradmag2.astype(np.uint8), markers)
        boundaries = L == 1
        #boundaries = ndimage.morphology.binary_fill_holes(boundaries, structure = np.ones((5, 5))).astype(int)
        re = image * ~boundaries
        ax1.imshow(image)
        ax2.imshow(re)
        plt.show()

        return result


ss = SkullStriping('recon_T1_synthetic_normal_1mm_L8_r2.mat')
#ss = SkullStriping('recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat')
ss.strip()

