clear all; close all;
%% Load Data
addpath .\Datasets\Data\
load diffusion_synthetic_normal_L8_r2_gr15_b1200.mat
% load T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat
% load T1_synthetic_normal_1mm_L8_r2.mat

%% Data: k-space > x-space
% Diffusion data: phase encoding x frequency encoding x gradient direction x receiver coil;
% raw_data(:,:,1,k) - baseline data from k-th channel;  
% raw_data(:,:,2:15,k) - diffusion-weighted images 
% with corresponding diffusion-sensitizing gradient directions from k-th channel
% MRI data: phase encoding x frequency encoding x receiver coil;
[Mx, My, S, L] = size(raw_data);

if L == 1
    L = S; clear S;
    type = 'conventional';
else
    type = 'diffusion';
end

raw_data = squeeze(raw_data); 

if size(raw_data,4) ~= 1
    for ss=1:S
        img_data(:,:,ss,:)=k_to_x(raw_data(:,:,ss,:), L);
    end
else
    img_data=k_to_x(raw_data, L);
end

%% Baseline image reconstruction
tic
SENSE_LSE = image_reconstruction(img_data, sensitivity_maps, r, L, 1);
toc
%%
% SENSE-Tikhonov reconstruction algorithm
lambda = 0.005;
SENSE_Tikhonov = image_reconstruction(img_data, sensitivity_maps, r, L, 2, lambda);

% SENSE-Tikhonov reconstruction algorithm with reference image
lambda_ref = 0.005;
% reference image choice 
% n=1 SENSE reconstruction image with Gaussian filtering
% n=2 SENSE reconstruction image with median filtering 
n=2;
switch n
case 1
    if size(raw_data,4) ~= 1
       for s=1:S
           filter = fspecial('gaussian', [3, 3], 2);
           reference_img(:,:,s) = conv2(SENSE_LSE(:,:,s), [5, 5]);
       end
    else
        filter = fspecial('gaussian', [3, 3], 2);
        reference_img = conv2(SENSE_LSE, [5, 5]);
    end
case 2
    if size(raw_data,4) ~= 1
       for s=1:S
           reference_img(:,:,s) = medfilt2(SENSE_LSE(:,:,s), [5, 5]);
       end
    else
        reference_img = medfilt2(SENSE_LSE, [5, 5]);
    end
end

SENSE_Tikhonov_ref = image_reconstruction(img_data, sensitivity_maps, r, L, 3, lambda_ref, reference_img);

%%
tic
SENSE_LSE_diffusion = image_reconstruction(img_data, sensitivity_maps, r, L, 4, lambda, image, gradients);
toc
%% Save data
% save('recon_T1_synthetic_normal_1mm_L8_r2', 'SENSE_LSE', 'SENSE_Tikhonov', 'SENSE_Tikhonov_ref_01');