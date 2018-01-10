clear all; close all;
%% Load Data
addpath .\Datasets\Data\
load diffusion_synthetic_normal_L8_r2_gr15_b1200.mat
% load T1_synthetic_multiple_sclerosis_lesions_1mm_L16_r2.mat
% load T1_synthetic_normal_1mm_L8_r2.mat

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

%%
lambda_vec = linspace(0.001,0.01,30);
%%
SENSE_LSE = image_reconstruction(img_data, sensitivity_maps, r, L, 1);
ND=ndims(SENSE_LSE);
if ND==2
   SENSE_Tikhonov = zeros(size(SENSE_LSE,1), size(SENSE_LSE,2),length(lambda_vec));
   SENSE_Tikhonov_ref = zeros(size(SENSE_LSE,1), size(SENSE_LSE,2),length(lambda_vec),2);
elseif ND==3
   SENSE_Tikhonov = zeros(size(SENSE_LSE,1), size(SENSE_LSE,2),S,length(lambda_vec));
   SENSE_Tikhonov_ref = zeros(size(SENSE_LSE,1), size(SENSE_LSE,2),S,length(lambda_vec),2);
end
%%
tic
for rr=1:2
    rr = 2;
    for kk=1:length(lambda_vec)
    
        lambda = lambda_vec(kk);
        % reference image
        switch rr
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
                   reference_img(:,1:256,s) = medfilt2(SENSE_LSE(:,:,s), [5, 5]);
               end
            else
                reference_img = medfilt2(SENSE_LSE, [5, 5]);
            end
        end
        
        if ND==2
           SENSE_Tikhonov(:,:,kk) = image_reconstruction(img_data, sensitivity_maps, r, L, 2, lambda);
           SENSE_Tikhonov_ref(:,:,rr,kk) = image_reconstruction(img_data, sensitivity_maps, r, L, 3, lambda, reference_img);
        elseif ND==3
           SENSE_Tikhonov(:,:,:,kk) = image_reconstruction(img_data, sensitivity_maps, r, L, 2, lambda);
           SENSE_Tikhonov_ref(:,:,:,kk,rr) = image_reconstruction(img_data, sensitivity_maps, r, L, 3, lambda, reference_img);
        end
    kk, rr 
    end
end
%%
