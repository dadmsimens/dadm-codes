%% Loading 3D volumes
clear all; close all;

% main source to read
source_path = './DATA/';


% T1, 1mm, INU=0%
[dataset_T1] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);

% T2, 1mm, INU=0%
[dataset_T2] = openBrainWebData([source_path 'T2/t2_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);

% PD, 1mm, INU=0%
[dataset_PD] = openBrainWebData([source_path 'PD/pd_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1);


% T1, 1mm, INU=20%
[dataset_T1_INU_20] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);

% T2, 1mm, INU=20%
[dataset_T2_INU_20] = openBrainWebData([source_path 'T2/t2_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);

% PD, 1mm, INU=20%
[dataset_PD_INU_20] = openBrainWebData([source_path 'PD/pd_icbm_normal_1mm_pn0_rf20.rawb'], 181, 217, 181, 1);



%% Visualization of single slices
% select one slice from the volumes and concatenate them all
text_size = 20;


% #1
slice = 40;
figure(1), imshow([dataset_T1(:,:,slice), dataset_T2(:,:,slice), dataset_PD(:,:,slice); dataset_T1_INU_20(:,:,slice), dataset_T2_INU_20(:,:,slice), dataset_PD_INU_20(:,:,slice)], []);
hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);


% #2
slice = 75;
figure(2), imshow([dataset_T1(:,:,slice), dataset_T2(:,:,slice), dataset_PD(:,:,slice); dataset_T1_INU_20(:,:,slice), dataset_T2_INU_20(:,:,slice), dataset_PD_INU_20(:,:,slice)], []);
hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);


% #3
slice = 90;
figure(3), imshow([dataset_T1(:,:,slice), dataset_T2(:,:,slice), dataset_PD(:,:,slice); dataset_T1_INU_20(:,:,slice), dataset_T2_INU_20(:,:,slice), dataset_PD_INU_20(:,:,slice)], []);
hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);


% #4
slice = 115;
figure(4), imshow([dataset_T1(:,:,slice), dataset_T2(:,:,slice), dataset_PD(:,:,slice); dataset_T1_INU_20(:,:,slice), dataset_T2_INU_20(:,:,slice), dataset_PD_INU_20(:,:,slice)], []);
hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);



%plot2svg('data_t1_t2_pd.svg', 1);

%% Show every 10 slices

for ii=1:10:150
    slice = ii;
    figure(ii), imshow([dataset_T1(:,:,slice), dataset_T2(:,:,slice), dataset_PD(:,:,slice); dataset_T1_INU_20(:,:,slice), dataset_T2_INU_20(:,:,slice), dataset_PD_INU_20(:,:,slice)], []);
    hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
    set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);
end




