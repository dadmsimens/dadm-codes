import matplotlib.pyplot as plt
from scipy.ndimage import morphology
from scipy.ndimage import label, watershed_ift, maximum_filter, sobel
from scipy.io import loadmat
import numpy as np
from strel import strel
from imimposemin import imimposemin


class SkullStriping:
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose

    def get_data(self):
        mat_dict = loadmat(self.filename)
        image = mat_dict['SENSE_Tikhonov']
        # image = mat_dict['SENSE_Tikhonov_ref_01']
        # image = mat_dict['SENSE_LSE']
        return image

    def grad_mag_sobel(self, image):
        # gradient magnitude using of the Sobel edge mask
        sx = sobel(image, axis=0, mode='constant')
        sy = sobel(image, axis=1, mode='constant')
        gradmag = np.hypot(sx, sy)
        return gradmag

    def foreground_markers(self, image):
        # mark the foreground objects
        i_erode = morphology.grey_erosion(image, 20)
        i_obr = morphology.grey_closing(i_erode, 10)
        i_obrd = morphology.grey_dilation(i_obr, 20)
        i_obrcbr = morphology.grey_closing(1 - i_obrd, 10)
        i_obrcbr = 1 - i_obrcbr
        neighborhood = morphology.generate_binary_structure(2, 2)
        fgm = maximum_filter(i_obrcbr, footprint=neighborhood)
        fgm2 = morphology.grey_closing(fgm, 5)
        fgm3 = morphology.grey_erosion(fgm2, 5)
        fgm4 = morphology.grey_opening(fgm3, 20)
        fgm4 = fgm4 >= 80
        return fgm4

    def background_markers(self, image):
        # mark the background objects
        threshold, upper, lower = 100, 1, 0
        bw = np.where(image > threshold, upper, lower)
        d = morphology.distance_transform_edt(bw)
        markers = label(bw)[0]
        dl = watershed_ift(d.astype(np.uint8), markers)
        bgm = dl == 1
        bgm = np.invert(bgm)
        se = strel('disk', 2)
        bgm = morphology.binary_opening(bgm, se)
        return bgm

    def watershed_skull_stripping(self):
        image = self.get_data()
        gradmag = self.grad_mag_sobel(image)
        log = self.foreground_markers(image)
        bgm = self.background_markers(image)
        gradmag2 = imimposemin(gradmag, bgm | log)
        markers = label(gradmag2)[0]
        l = watershed_ift(gradmag2.astype(np.uint8), markers)
        boundaries = l == 0
        if self.verbose:
            fig = plt.figure()
            plt.gray()
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            result = image * boundaries
            ax1.imshow(image)
            ax2.imshow(result)
            plt.show()
        return boundaries

if __name__ == '__main__':
    # ss = SkullStriping('recon_T1_synthetic_normal_1mm_L8_r2.mat', verbose=True)
    ss = SkullStriping('recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat', verbose=True)
    # ss = SkullStriping('brain.mat', verbose=True)
    ss.watershed_skull_stripping()

