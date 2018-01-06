clear all
close all
filename = 'dane\recon_T1_synthetic_normal_1mm_L8_r2.mat'
%filename = 'dane\recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat'
%filename = 'dane\recon_dMRI_synthetic_normal_L8_r2_gr15_b1200.mat'
[image,image2,image3] = loadData(filename);
brain = skull_watershed(image3);
figure
subplot(1,2,1)
imshow(image3)
title('Input image')
subplot(1,2,2)
imshow(brain)
title('After watershed marked-controll algorithm')
figure
mask = zeros(size(image));
mask(25:end-25,25:end-25) = 1;
i_2 = activecontour(brain,mask);
imshow(i_2)
