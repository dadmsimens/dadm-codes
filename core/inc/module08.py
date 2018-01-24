import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import morphology, center_of_mass, find_objects, maximum, minimum
from scipy.ndimage import label, watershed_ift, maximum_filter, sobel
from . import simens_dadm as smns


class SkullStripping:
    def __init__(self, image):
        self.image = image

    def recon(self, marker, mask):
        recon = marker
        recon1_old = np.zeros_like(self.image)
        while sum(sum(recon - recon1_old)) != 0:
            recon1_old = recon
            recon = ndimage.grey_dilation(recon, 5)
            bw = recon > mask
            recon[bw] = mask[bw]
        return recon

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

    def csf_counting(self):
        pixel_counts, gray_levels = np.histogram(self.image)
        upcut = 0.98 * maximum(gray_levels)
        downcut = 0.02 * maximum(gray_levels)
        for i in range(0, len(gray_levels)-1):
            if (gray_levels.item(i) < downcut) or (gray_levels.item(i) > upcut):
                pixel_counts[i] = 0
        csf = 0.1 * (maximum(gray_levels) - minimum(gray_levels[gray_levels > 0])) + minimum(gray_levels[gray_levels> 0])
        return csf

    def binarization(self, image, threshold, upper=1, lower=0):
        bin_image = np.where(image >= threshold, upper, lower)
        return bin_image

    def radius_counting(self, bin_image):
        bboxes = find_objects(bin_image.astype(np.uint8))[0]
        y = bboxes[0]
        x = bboxes[1]
        diamx = x.stop - x.start
        diamy = y.stop - y.start
        st = diamx / diamy
        diameters = np.mean([diamx, diamy])
        r = diameters / 2
        return r, st

    def preprocessing(self):
        # preprocessing to get cfs and crop image
        csf = self.csf_counting()
        bin_image = self.binarization(self.image, csf)
        se = self.strel('disk', 1)
        bin = morphology.binary_erosion(bin_image, se)
        cog = center_of_mass(bin, self.image)
        r, st = self.radius_counting(bin)
        [xx, yy] = np.mgrid[(1-cog[0]):(len(self.image)+1-cog[0]), (1-cog[1]):(len(self.image)+1-cog[1])]
        mask = (xx ** 2 + yy ** 2) < r ** 2
        cropped_image = self.image * mask
        return cropped_image, csf, cog, r, st

    def grad_mag_sobel(self, image):
        # gradient magnitude using of the Sobel edge mask
        sx = sobel(image, axis=0, mode='constant')
        sy = sobel(image, axis=1, mode='constant')
        gradmag = np.hypot(sx, sy)
        return gradmag

    def anisodiff(self, image, niter=1, kappa=50, gamma=0.1, step=(1., 1.), option=1):
        image = image.astype('float32')
        image_out = image.copy()
        deltaS = np.zeros_like(image_out)
        deltaE = deltaS.copy()
        NS = deltaS.copy()
        EW = deltaS.copy()
        gS = deltaS.copy()
        gE = deltaS.copy()
        for i in range(niter):
            deltaS[:-1, :] = np.diff(image_out, axis=0)
            deltaE[:, :-1] = np.diff(image_out, axis=1)
            if option == 1:
                gS = np.exp(-(deltaS / kappa) ** 2.) / step[0]
                gE = np.exp(-(deltaE / kappa) ** 2.) / step[1]
            elif option == 2:
                gS = 1. / (1. + (deltaS / kappa) ** 2.) / step[0]
                gE = 1. / (1. + (deltaE / kappa) ** 2.) / step[1]
            e = gE * deltaE
            s = gS * deltaS
            NS[:] = s
            EW[:] = e
            NS[1:, :] -= s[:-1, :]
            EW[:, 1:] -= e[:, :-1]
            image_out += gamma * (NS + EW)
        return image_out

    def edges_marr_hildreth(self, image, sigma):
        size = int(2 * (np.ceil(3 * sigma)) + 1)
        x, y = np.meshgrid(np.arange(-size / 2 + 1, size / 2 + 1), np.arange(-size / 2 + 1, size / 2 + 1))
        normal = 1 / (2.0 * np.pi * sigma ** 2)
        kernel = ((x ** 2 + y ** 2 - (2.0 * sigma ** 2)) / sigma ** 4) * np.exp(
            -(x ** 2 + y ** 2) / (2.0 * sigma ** 2)) / normal
        kern_size = kernel.shape[0]
        log = np.zeros_like(image, dtype=float)
        for i in range(image.shape[0] - (kern_size - 1)):
            for j in range(image.shape[1] - (kern_size - 1)):
                window = image[i:i + kern_size, j:j + kern_size] * kernel
                log[i, j] = np.sum(window)
        log = log.astype(np.int64, copy=False)
        zero_crossing = np.zeros_like(log)
        for i in range(log.shape[0] - (kern_size - 1)):
            for j in range(log.shape[1] - (kern_size - 1)):
                if log[i][j] == 0:
                    if (log[i][j - 1] < 0 and log[i][j + 1] != 0) or (log[i - 1][j] < 0 and log[i + 1][j] > 0) or (log[i - 1][j] > 0 and log[i + 1][j] < 0):
                        zero_crossing[i][j] = 255
                if log[i][j] < 0:
                    if (log[i][j - 1] > 0) or (log[i][j + 1] > 0) or (log[i - 1][j] > 0) or (log[i + 1][j] > 0):
                        zero_crossing[i][j] = 255
        return zero_crossing

    def background_markers(self, preproc_image, csf):
        # mark the background markers
        bw = self.binarization(preproc_image, csf, 0, 1)
        d = morphology.distance_transform_edt(bw)
        dl = watershed_ift(bw.astype(np.uint8), d.astype(np.int16))
        bgm = dl == 1
        bgm = np.invert(bgm)
        return bgm

    def foreground_markers(self, preproc_image, csf):
        # mark the foreground objects
        i_erode = morphology.grey_erosion(preproc_image, 20)
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

    def watershed(self, preproc_image, csf, cog):
        gradmag = self.grad_mag_sobel(preproc_image)
        fgm = self.foreground_markers(preproc_image, csf)
        bgm = self.background_markers(preproc_image, csf)
        markers = np.zeros_like(preproc_image).astype(np.int16)
        markers[bgm == False] = 1
        markers[fgm == True] = 2
        l = watershed_ift(gradmag.astype(np.uint8), markers)
        brain = l == l[cog[0].astype(np.int), cog[1].astype(np.int)]
        return brain

    def bse(self, cog):
        filtered_image = self.anisodiff(self.image, 3)
        marr_h = self.edges_marr_hildreth(filtered_image, 0.6)
        marr_hi = marr_h == 0
        # romb = np.array(
        #     [[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1],
        #      [0, 1, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0]])
        marr_hie = morphology.binary_erosion(marr_hi, structure=np.ones([7, 7]))
        markers = label(marr_hie)[0]
        l = watershed_ift(marr_hie.astype(np.uint8), markers)
        boundaries = l == l[cog[0].astype(np.int), cog[1].astype(np.int)]
        b_d = morphology.binary_dilation(boundaries, structure=np.ones([7, 7]))
        brain = morphology.binary_closing(b_d, structure=self.strel('disk', 15))
        return brain

    def run(self, verbose=False, diff=False):
        preproc_image, csf, cog, r, st = self.preprocessing()
        if r <= 56 or st > 1.3:
            skull_stripping_mask = np.zeros_like(self.image)
        else:
            skull_stripping_mask = self.bse(cog)
            check = np.sum(skull_stripping_mask)
            if check < 4000 or check > np.pi * r**2 or diff:
                skull_stripping_mask = self.watershed(preproc_image, csf, cog)
        if verbose:
            plt.figure()
            plt.imshow(self.image, 'gray', interpolation='none')
            plt.imshow(skull_stripping_mask, 'jet', interpolation='none', alpha=0.5)
            plt.show()
        return skull_stripping_mask


def main8(mri_input, verbose=False):
    if isinstance(mri_input, smns.mri_diff):  # instructions for diffusion mri
        [m, n, slices] = mri_input.structural_data.shape
        data_output_struct = np.zeros([m, n, slices])
        for i in range(slices):
            data_output_struct[:, :, i] = SkullStripping(mri_input.structural_data[:, :, i]).run(verbose, diff=True)
        mri_input.skull_stripping_mask = data_output_struct

    elif isinstance(mri_input, smns.mri_struct):
        [m, n, slices] = mri_input.structural_data.shape
        data_output_struct = np.zeros([m, n, slices])
        for i in range(slices):
            data_output_struct[:, :, i] = SkullStripping(mri_input.structural_data[:, :, i]).run(verbose)
        mri_input.skull_stripping_mask = data_output_struct
    else:
        return "Unexpected data format in module number 8!"
    return mri_input


def skull_stripped_image(mri_input):
    if isinstance(mri_input, smns.mri_diff):
        [m, n, slices, grad] = mri_input.diffusion_data.shape
        data_output_diff = np.zeros([m, n, slices, grad])
        for i in range(slices):
            for j in range(grad):
                data_output_diff[:, :, i, j] = mri_input.skull_stripping_mask[:, :, i] * mri_input.diffusion_data[:, :, i, j]
        mri_input.diffusion_data = data_output_diff

        [m, n, slices] = mri_input.structural_data.shape
        data_output_struct = np.zeros([m, n, slices])
        for i in range(slices):
            data_output_struct[:, :, i] = mri_input.skull_stripping_mask[:, :, i] * mri_input.structural_data[:, :, i]
        mri_input.structural_data = data_output_struct
    elif isinstance(mri_input, smns.mri_struct):
        [m, n, slices] = mri_input.structural_data.shape
        data_output_struct = np.zeros([m, n, slices])
        for i in range(slices):
            data_output_struct[:, :, i] = mri_input.skull_stripping_mask[:, :, i] * mri_input.structural_data[:, :, i]
        mri_input.structural_data = data_output_struct
    else:
        return "Unexpected data format in module number 8!"
    return mri_input
