%% SENSE RECONSTRUCTION - BrainWebDATA: brainweb.bic.mni.mcgill.ca/brainweb/
clear all; close all;

%% 1. Load data
% source path for synthetic data
source_path = 'Datasets/Synthetic_BrainWeb/DATA/';

% INU=0%
% [dataset_T1] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);
% [dataset_T2] = openBrainWebData([source_path 'T2/t2_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);
% [dataset_PD] = openBrainWebData([source_path 'PD/pd_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);

% INU=20%
% [dataset_T1_INU_20] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);
% [dataset_T2_INU_20] = openBrainWebData([source_path 'T2/t2_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);
% [dataset_PD_INU_20] = openBrainWebData([source_path 'PD/pd_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);

% INU=40%
[dataset_T1_INU_40] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf40.rawb'], 181, 217, 181, 1);
% [dataset_T2_INU_40] = openBrainWebData([source_path 'T2/t2_icbm_normal_1mm_pn0_rf40.rawb'], 181, 217, 181, 1);
% [dataset_PD_INU_40] = openBrainWebData([source_path 'PD/pd_icbm_normal_1mm_pn0_rf40.rawb'], 181, 217, 181, 1);

slice = 81; % slice choice - values from 1 to 181
image = dataset_T1_INU_40(:,:,slice); % change name for different projections

image = image./max(image(:)).*255; % normalize the data
figure, imshow(image, []); 

%% 2. Set reconstruction parameters
close all;
% subsampling rates, values: 2, 4, 8 (condition: r < L)
r = 2;
% number of receiver coils: >= 4
nc = 8; 
% mask
mask = open('mask.mat'); i_mask = mask.i_mask; clear mask;
% % calculate a binary mask
% % se = strel('disk', 5); i_mask1 = imclose(image > 25, se); 

%% 3. Sensitivity maps
% smooth sensitivity maps (synthetic) - a priori assumption 
[Mx, My] = size(image);	
SynthMaps = sensitivity_map([Mx, My], nc, 0.75);

figure, 
imshow([real([SynthMaps(:,:,1),SynthMaps(:,:,2),SynthMaps(:,:,3),SynthMaps(:,:,4);
             SynthMaps(:,:,5),SynthMaps(:,:,6),SynthMaps(:,:,7),SynthMaps(:,:,8)]);
       imag([SynthMaps(:,:,1),SynthMaps(:,:,2),SynthMaps(:,:,3),SynthMaps(:,:,4);
             SynthMaps(:,:,5),SynthMaps(:,:,6),SynthMaps(:,:,7),SynthMaps(:,:,8)])], []); colorbar;       
% figure, imshow(abs(SynthMaps(:,:,1)),[]); colorbar;
% figure, imshow(sum(abs(SynthMaps).^2, 3), []); colorbar;

%% 4. Add noise and sensitivity coils profiles to data
close all;
% normally distributed noise in each coil in x-space domain 
std = 10;
% correlation between receiver coils
rho = 0.2;
% data simulated (ds) in x-space in each receiver coil
[data_sim, noise] = noisy_data(image, nc, SynthMaps, std, rho);

% noise components > different in each coil !
figure, 
imshow([noise(:,:,1), noise(:,:,2), noise(:,:,3), noise(:,:,4);  
        noise(:,:,5), noise(:,:,6), noise(:,:,7), noise(:,:,8)], []);
colorbar;

% simulated MRI data
figure, 
imshow([abs(data_sim(:,:,1)), abs(data_sim(:,:,2)), abs(data_sim(:,:,3)), abs(data_sim(:,:,4));
        abs(data_sim(:,:,5)), abs(data_sim(:,:,6)), abs(data_sim(:,:,7)), abs(data_sim(:,:,8))], []);
caxis([0, 90]); colorbar;

% reference SoS image - with noise
sos_img = sos(data_sim);
% ref_img = sos_img.*i_mask;

figure, imshow(sos_img, []);

%% 5. Data in k-space domain
% kData = x_to_k(data_sim, nc);
% 
% figure, 
% imshow(log(([abs(kData(:,:,1)), abs(kData(:,:,2)), abs(kData(:,:,3)), abs(kData(:,:,4));  
%              abs(kData(:,:,5)), abs(kData(:,:,6)), abs(kData(:,:,7)), abs(kData(:,:,8))])+1), []);
% colorabr;

%% 6. Prepare data for reconstruction
close all;
xData_subsamp = data_preparation(data_sim, nc, r);
% xData_subsamp_moved = movedata(xData_subsamp, r);
% xData_subsamp = xData_subsamp_moved;

figure, 
imshow(abs([xData_subsamp(:,:,1),xData_subsamp(:,:,2),xData_subsamp(:,:,3),xData_subsamp(:,:,4),...
            xData_subsamp(:,:,5),xData_subsamp(:,:,6),xData_subsamp(:,:,7),xData_subsamp(:,:,8)]),[]); colorbar;
% figure, imshow(abs(xData_subsamp(:,:,1)), []); colorbar;

%% 7. SENSE reconstruction 
close all;
% with different methods applied: BASIC SENSE (LSE) and Tikhonov regularization

kData_subsamp = x_to_k(xData_subsamp, nc);

% SENSE basic reconstruction (no correlations between coils and variance equal in each coil)
SENSE_SigMat = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 1, rho, std);

% SENSE basic reconstruction with covariance matrix between coils
SENSE_CovMat = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 2, rho, std);

% SENSE reconstruction with LSE method
SENSE_LSE = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 3, rho, std);

% SENSE-Tikhonov reconstruction algorithm
% lambda = 0.05;
% SENSE_Tikhonov = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 4, rho, std, lambda);

SENSE_Tikhonov_005 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 4, rho, std, 0.05);
SENSE_Tikhonov_008 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 4, rho, std, 0.08);
SENSE_Tikhonov_01 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 4, rho, std, 0.1);
SENSE_Tikhonov_012 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 4, rho, std, 0.12);
SENSE_Tikhonov_015 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 4, rho, std, 0.2);
SENSE_Tikhonov_018 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 4, rho, std, 0.25);

% SENSE-Tikhonov reconstruction algorithm with reference image
% lambda_ref = 0.25;

% reference image choice 
% 1) SENSE reconstruction image with Gaussian filtering
% filter = fspecial('gaussian', [3, 3], 2); 
%reference_img = conv2(SENSE_SigMat, filter, 'same');
% 2) SENSE reconstruction image with median filtering 
reference_img = medfilt2(SENSE_SigMat, [5, 5]);

% different lambda
SENSE_Tikhonov_ref_005 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 5, rho, std, 0.05, reference_img);
SENSE_Tikhonov_ref_008 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 5, rho, std, 0.08, reference_img);
SENSE_Tikhonov_ref_01 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 5, rho, std, 0.1, reference_img);
SENSE_Tikhonov_ref_012 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 5, rho, std, 0.12, reference_img);
SENSE_Tikhonov_ref_015 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 5, rho, std, 0.2, reference_img);
SENSE_Tikhonov_ref_018 = image_reconstruction(kData_subsamp, SynthMaps, r, nc, 5, rho, std, 0.25, reference_img);

%% 8. Present reconstructed images 

% data_reference = ones(256, 512);
% data_reference(:, 129:384) = sos_img;

% SENSE_SigMat = SENSE_SigMat.*i_mask;
% SENSE_CovMat = SENSE_CovMat.*i_mask;
% SENSE_LSE = SENSE_LSE.*i_mask;
% SENSE_Tikhonov_005 = SENSE_Tikhonov_005.*i_mask;
% SENSE_Tikhonov_008 = SENSE_Tikhonov_008.*i_mask;
% SENSE_Tikhonov_01 = SENSE_Tikhonov_01.*i_mask;
% SENSE_Tikhonov_012 = SENSE_Tikhonov_012.*i_mask;
% SENSE_Tikhonov_015 = SENSE_Tikhonov_015.*i_mask;
% SENSE_Tikhonov_018 = SENSE_Tikhonov_018.*i_mask;
% SENSE_Tikhonov_ref_005 = SENSE_Tikhonov_ref_005.*i_mask;
% SENSE_Tikhonov_ref_008 = SENSE_Tikhonov_ref_008.*i_mask;
% SENSE_Tikhonov_ref_01 = SENSE_Tikhonov_ref_01.*i_mask;
% SENSE_Tikhonov_ref_012 = SENSE_Tikhonov_ref_012.*i_mask;
% SENSE_Tikhonov_ref_015 = SENSE_Tikhonov_ref_015.*i_mask;
% SENSE_Tikhonov_ref_018 = SENSE_Tikhonov_ref_018.*i_mask;

% SENSE_CovMat(SENSE_CovMat>800) = 800;

% figure,
% imshow([SENSE_Tikhonov_005, SENSE_Tikhonov_008, SENSE_Tikhonov_01;...
%         SENSE_Tikhonov_012, SENSE_Tikhonov_015, SENSE_Tikhonov_018], []);
% colorbar; colormap('jet');
% 
% figure,
% imshow([SENSE_Tikhonov_ref_005, SENSE_Tikhonov_ref_008, SENSE_Tikhonov_ref_01;...
%         SENSE_Tikhonov_ref_012, SENSE_Tikhonov_ref_015, SENSE_Tikhonov_ref_018], []);
% colorbar; colormap('jet');

% % title(['Reconstruction of an image with n_coils=', num2str(L), ' coils and subsampling rate subsamp_rate=', num2str(r)]);
% text_size = 16;  set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);

%% 9. Checking the errors of reconstructed images

%error maps
SENSE_SigMat_SoS = abs(SENSE_SigMat - sos_img).* i_mask;
SENSE_CovMat_SoS = abs(SENSE_CovMat - sos_img).* i_mask;
SENSE_LSE_SoS = abs(SENSE_LSE - sos_img).* i_mask;
SENSE_Tikhonov_005_SoS =  abs(SENSE_Tikhonov_005 - sos_img).* i_mask;
SENSE_Tikhonov_008_SoS =  abs(SENSE_Tikhonov_008 - sos_img).* i_mask;
SENSE_Tikhonov_01_SoS =  abs(SENSE_Tikhonov_01 - sos_img).* i_mask;
SENSE_Tikhonov_012_SoS =  abs(SENSE_Tikhonov_012 - sos_img).* i_mask;
SENSE_Tikhonov_015_SoS =  abs(SENSE_Tikhonov_015 - sos_img).* i_mask;
SENSE_Tikhonov_018_SoS =  abs(SENSE_Tikhonov_018 - sos_img).* i_mask;
SENSE_Tikhonov_ref_005_SoS =  abs(SENSE_Tikhonov_ref_005 - sos_img).* i_mask;
SENSE_Tikhonov_ref_008_SoS =  abs(SENSE_Tikhonov_ref_008 - sos_img).* i_mask;
SENSE_Tikhonov_ref_01_SoS =  abs(SENSE_Tikhonov_ref_01 - sos_img).* i_mask;
SENSE_Tikhonov_ref_012_SoS =  abs(SENSE_Tikhonov_ref_012 - sos_img).* i_mask;
SENSE_Tikhonov_ref_015_SoS =  abs(SENSE_Tikhonov_ref_015 - sos_img).* i_mask;
SENSE_Tikhonov_ref_018_SoS =  abs(SENSE_Tikhonov_ref_018 - sos_img).* i_mask;


figure,
imshow([SENSE_SigMat_SoS, zeros(256,256), SENSE_LSE_SoS;...
        SENSE_Tikhonov_005_SoS, SENSE_Tikhonov_008_SoS, SENSE_Tikhonov_01_SoS;...
        SENSE_Tikhonov_012_SoS, SENSE_Tikhonov_015_SoS, SENSE_Tikhonov_018_SoS;...
        SENSE_Tikhonov_ref_005_SoS, SENSE_Tikhonov_ref_008_SoS, SENSE_Tikhonov_ref_01_SoS;...
        SENSE_Tikhonov_ref_012_SoS, SENSE_Tikhonov_ref_015_SoS, SENSE_Tikhonov_ref_018_SoS], []);
    colorbar; colormap(hot); 

    
SENSE_SigMat_SoS1 = SENSE_SigMat_SoS(SENSE_SigMat_SoS>0);
SENSE_CovMat_SoS1 = SENSE_CovMat_SoS(SENSE_CovMat_SoS>0);
SENSE_LSE_SoS1 = SENSE_LSE_SoS(SENSE_LSE_SoS>0);

SENSE_Tikhonov_005_SoS1 = SENSE_Tikhonov_005_SoS(SENSE_Tikhonov_005_SoS > 0);
SENSE_Tikhonov_008_SoS1 = SENSE_Tikhonov_008_SoS(SENSE_Tikhonov_008_SoS > 0);
SENSE_Tikhonov_01_SoS1 = SENSE_Tikhonov_01_SoS(SENSE_Tikhonov_01_SoS > 0);
SENSE_Tikhonov_012_SoS1 = SENSE_Tikhonov_012_SoS(SENSE_Tikhonov_012_SoS > 0);
SENSE_Tikhonov_015_SoS1 = SENSE_Tikhonov_015_SoS(SENSE_Tikhonov_015_SoS > 0);
SENSE_Tikhonov_018_SoS1 = SENSE_Tikhonov_018_SoS(SENSE_Tikhonov_018_SoS > 0);

SENSE_Tikhonov_ref_005_SoS1 = SENSE_Tikhonov_ref_005_SoS(SENSE_Tikhonov_ref_005_SoS > 0);
SENSE_Tikhonov_ref_008_SoS1 = SENSE_Tikhonov_ref_008_SoS(SENSE_Tikhonov_ref_008_SoS > 0);
SENSE_Tikhonov_ref_01_SoS1 = SENSE_Tikhonov_ref_01_SoS(SENSE_Tikhonov_ref_01_SoS > 0);
SENSE_Tikhonov_ref_012_SoS1 = SENSE_Tikhonov_ref_012_SoS(SENSE_Tikhonov_ref_012_SoS > 0);
SENSE_Tikhonov_ref_015_SoS1 = SENSE_Tikhonov_ref_015_SoS(SENSE_Tikhonov_ref_015_SoS > 0);
SENSE_Tikhonov_ref_018_SoS1 = SENSE_Tikhonov_ref_018_SoS(SENSE_Tikhonov_ref_018_SoS > 0);


ref_error(1,1) = norm(SENSE_SigMat_SoS1(:));
ref_error(1,2) = norm(SENSE_CovMat_SoS1(:));
ref_error(1,3) = norm(SENSE_LSE_SoS1(:));

ref_error(1,4) = norm(SENSE_Tikhonov_005_SoS1(:));
ref_error(1,5) = norm(SENSE_Tikhonov_008_SoS1(:));
ref_error(1,6) = norm(SENSE_Tikhonov_01_SoS1(:));
ref_error(1,7) = norm(SENSE_Tikhonov_012_SoS1(:));
ref_error(1,8) = norm(SENSE_Tikhonov_015_SoS1(:));
ref_error(1,9) = norm(SENSE_Tikhonov_018_SoS1(:));

ref_error(1,10) = norm(SENSE_Tikhonov_ref_005_SoS1(:));
ref_error(1,11) = norm(SENSE_Tikhonov_ref_008_SoS1(:));
ref_error(1,12) = norm(SENSE_Tikhonov_ref_01_SoS1(:));
ref_error(1,13) = norm(SENSE_Tikhonov_ref_012_SoS1(:));
ref_error(1,14) = norm(SENSE_Tikhonov_ref_015_SoS1(:));
ref_error(1,15) = norm(SENSE_Tikhonov_ref_018_SoS1(:));


ref_error
