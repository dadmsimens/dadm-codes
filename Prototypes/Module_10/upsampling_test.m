clear all
close all
clc

m=matfile('recon_T1_synthetic_normal_1mm_L8_r2.mat');
image=m.SENSE_LSE;
upsampled=upsampling(image, 2, 2, 2);
save('upsampled.mat', 'upsampled');
save('original.mat', 'image');