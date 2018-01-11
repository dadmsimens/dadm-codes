import matplotlib.pyplot as plt
from scipy.ndimage import morphology, center_of_mass, find_objects, maximum, minimum
from scipy.ndimage import label, watershed_ift, maximum_filter, sobel
from scipy.io import loadmat, savemat
import numpy as np
from strel import strel
from imimposemin import imimposemin


class SkullStriping:
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose

    def get_data(self, all = False):
        if True == all:
            mat_dict = loadmat(self.filename)
            image = mat_dict['SENSE_LSE']
        else:
            mat_dict = loadmat(self.filename)
            image = mat_dict['SENSE_Tikhonov']
            # image = mat_dict['SENSE_Tikhonov_ref_01']
            # image = mat_dict['SENSE_LSE']
        return image

    def preprocessing(self, image):
        #preprocessing to get cfs and crop image
        se = strel('disk', 1)
        imag = morphology.grey_erosion(image, 5)
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
        labels = label(bin)[0]
        bboxes = find_objects(labels)[0]
        y = bboxes[0]
        x = bboxes[1]
        diamx = x.stop - x.start + 20
        diamy = y.stop - y.start + 20
        diameters = np.mean([diamx, diamy])
        r = diameters / 2

        [xx, yy] = np.mgrid[(1-cog[0]):(257-cog[0]), (1-cog[1]):(257-cog[1])]
        mask = (xx ** 2 + yy ** 2) < r ** 2
        cropped_image = image * mask
        # fig = plt.figure()
        # plt.gray()
        # ax1 = fig.add_subplot(121)
        # ax2 = fig.add_subplot(122)
        # ax1.imshow(mask)
        # ax2.imshow(cropped_image)
        # plt.show()
        return cropped_image, csf

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
        threshold, upper, lower = csf, 1, 0
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
        image = self.get_data(all=True)
        if 3 == len(image.shape):
            boundaries = np.zeros((256, 256, 181))
            for i in range(0, 180):
                preproc_image, csf = self.preprocessing(image[:, :, i])
                gradmag = self.grad_mag_sobel(preproc_image)
                log = self.foreground_markers(preproc_image, csf)
                bgm = self.background_markers(preproc_image, csf)
                gradmag2 = imimposemin(gradmag, bgm | log)
                markers = label(gradmag2)[0]
                l = watershed_ift(gradmag2.astype(np.uint8), markers)
                boundaries[:, :, i] = l == 0
                if self.verbose:
                    fig = plt.figure()
                    plt.gray()
                    ax1 = fig.add_subplot(121)
                    ax2 = fig.add_subplot(122)
                    result = image[:, :, i] * boundaries[:, :, i]
                    saving = {"skull_stripped": result}
                    savemat('skull_stripped2.mat', saving)
                    ax1.imshow(image[:, :, i])
                    ax2.imshow(result)
                    plt.show()
        else:
            preproc_image, csf = self.preprocessing(image)
            gradmag = self.grad_mag_sobel(preproc_image)
            log = self.foreground_markers(preproc_image, csf)
            bgm = self.background_markers(preproc_image, csf)
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
                saving = {"skull_stripped": result}
                savemat('skull_stripped2.mat', saving)
                ax1.imshow(image)
                ax2.imshow(result)
                plt.show()
        return boundaries

if __name__ == '__main__':
    ss = SkullStriping('recon_T1_synthetic_normal_1mm_L8_r2.mat', verbose=True)
    # ss = SkullStriping('recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat', verbose=True)
    # ss = SkullStriping('brain.mat')
    # ss = SkullStriping('SENSE_LSE_L_8_r_2_STD_2_RHO_0.mat', verbose=True)
    ss.watershed_skull_stripping()


