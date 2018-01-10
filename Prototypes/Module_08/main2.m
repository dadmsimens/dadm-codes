clear all
close all
% Main withot showing each step for hole scan
%filename = 'dane\recon_T1_synthetic_normal_1mm_L8_r2.mat'
%filename = 'dane\recon_T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat'
%filename = 'dane\recon_dMRI_synthetic_normal_L8_r2_gr15_b1200.mat'
%filename2 = 'dane\SENSE_LSE_L_8_r_2_STD_2_RHO_0 (4).mat'
%[image,image2,image3] = loadData(filename);
load('dane\SENSE_LSE_L_8_r_2_STD_2_RHO_0.mat')
imshow3D(SENSE_LSE)
brain = zeros(256,256,181);
for i = 1:181
     brain(:,:,i) = skull_watershed_prepoc(mat2gray(SENSE_LSE(:,:,i)), i);
     if i == 90
         i
     end
 end
figure
imshow3D(brain)
% subplot(1,2,1)
% imshow(image3(:,:,1))
% title('Input image')
% subplot(1,2,2)
% imshow(brain)
% title('After watershed marked-controll algorithm')
