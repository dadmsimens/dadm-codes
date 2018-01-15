import matplotlib.pyplot as plt
from scipy.ndimage import morphology, center_of_mass, find_objects, maximum, minimum
from scipy.ndimage import watershed_ift, maximum_filter, sobel
import numpy as np
from scipy import ndimage
from . import simens_dadm as smns

class SkullStripping:
    def __init__(self, image):
        self.image = image

    def recon(self, marker, mask):
        recon1 = marker
        recon1_old = np.zeros([256, 256], 'uint8')
        while sum(sum(recon1 - recon1_old)) != 0:
            recon1_old = recon1
            recon1 = ndimage.grey_dilation(recon1, 5)
            bw = recon1 > mask
            recon1[bw] = mask[bw]
        return recon1

    def strel(self, type, size):
        a, b = size, size
        n = 2 * size + 1
        if type == 'disk':
            y, x = np.ogrid[-a:n - a, -b:n - b]
            mask = x * x + y * y <= size * size
            array = np.ones((size * 2 + 1, size * 2 + 1))
            array[mask] = 0
        elif type == 'array':
            mask = np.ones((a, b), dtype=bool)
            array = np.ones((a, b))
            array[mask] = 0
        return array

    def preprocessing(self, image):
        #preprocessing to get cfs and crop image
        se = self.strel('disk', 1)
        imag = image
        pixel_counts, gray_levels = np.histogram(imag, bins=256)
        upcut = 0.98 * maximum(gray_levels)
        downcut = 0.02 * maximum(gray_levels)
        for i in range(0, len(gray_levels)-1):
            if (gray_levels.item(i) < downcut) or (gray_levels.item(i) > upcut):
                pixel_counts[i] = 0
        csf = 0.1 * (maximum(gray_levels) - minimum(gray_levels[gray_levels > 0])) + minimum(gray_levels[gray_levels> 0])
        threshold, upper, lower = csf, 1, 0
        bin = np.where(image > threshold, upper, lower)
        bin = morphology.binary_erosion(bin, se)
        cog = center_of_mass(bin, image)
        bboxes = find_objects(bin.astype(np.uint16))[0]
        y = bboxes[0]
        x = bboxes[1]
        diamx = x.stop - x.start
        diamy = y.stop - y.start
        diameters = np.mean([diamx, diamy])
        r = diameters / 2 + 10
        [xx, yy] = np.mgrid[(1-cog[0]):(257-cog[0]), (1-cog[1]):(257-cog[1])]
        mask = (xx ** 2 + yy ** 2) < r ** 2
        cropped_image = image * mask
        return cropped_image, csf, cog, r

    def grad_mag_sobel(self, image):
        # gradient magnitude using of the Sobel edge mask
        sx = sobel(image, axis=0, mode='constant')
        sy = sobel(image, axis=1, mode='constant')
        gradmag = np.hypot(sx, sy)
        return gradmag

    def foreground_markers(self, image, csf):
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
        fgm4 = fgm4 >= csf
        return fgm4

    def background_markers(self, image, csf):
        # mark the background objects
        threshold, upper, lower = csf+20, 0, 1
        bw = np.where(image >= threshold, upper, lower)
        d = morphology.distance_transform_edt(bw)
        dl = watershed_ift(bw.astype(np.uint8), d.astype(np.int16))
        bgm = dl == 1
        bgm = np.invert(bgm)
        return bgm

    def run(self, verbose=False):
        skull_stripp_mask = np.zeros_like(self.image)
        preproc_image, csf, cog, r = self.preprocessing(self.image)
        gradmag = self.grad_mag_sobel(preproc_image)
        log = self.foreground_markers(preproc_image, csf)
        bgm = self.background_markers(preproc_image, csf)
        markers = np.zeros_like(self.image).astype(np.int16)
        markers[bgm == False] = 1
        markers[log == True] = 2
        l = watershed_ift(gradmag.astype(np.uint16), markers)
        skull_stripp_mask = l == l[cog[0].astype(np.int), cog[1].astype(np.int)]
        if verbose:
            fig = plt.figure()
            plt.gray()
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)
            result = self.image * skull_stripp_mask
            ax1.imshow(self.image)
            ax2.imshow(result)
            plt.show()
        return skull_stripp_mask


def main8(mri_input, verbose=False):
    if isinstance(mri_input, smns.mri_diff):  # instructions for diffusion mri
        mri_output = mri_input
        for i in range(mri_input.diffusion_data.shape[2]):
            mri_output.skull_stripping_mask = SkullStripping(mri_input.diffusion_data[:, :, 1]).run(verbose)
        print("This file contains diffusion MRI")
        # it should works, I make tests when 3D data will be available,
    elif isinstance(mri_input, smns.mri_struct):
        print("This file contains structural MRI")
        mri_output = mri_input
        mri_output.skull_stripping_mask = SkullStripping(mri_input.structural_data).run(verbose)
    else:
        return "Unexpected data format in module number 8!"
    return mri_output
