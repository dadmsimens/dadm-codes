%% Loading 3D volumes and anatomical model
clear all; close all;

% main source to read
source_path = './DATA/';


% load single volume
[dataset_T1] = openBrainWebData([source_path 'T1/t1_icbm_normal_1mm_pn0_rf0.rawb'], 181, 217, 181, 1); % T1, 1mm, INU=0%

% load anatomical model
[anatomical_model] = openAnatomicalModel([source_path 'AnatomicalModel/phantom_1.0mm_normal_crisp.rawb'], 181, 217, 181, 1); % anatomical model



%% 1. Visualization of single slices and anatomical models for them
% select one slice from the volumes and concatenate them all
text_size = 20;


% magnitude data
figure(1), imshow([dataset_T1(:,:,60), dataset_T1(:,:,75), dataset_T1(:,:,90), dataset_T1(:,:,115)], []);
hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);

% corresponding anatomical model
figure(2), imshow([anatomical_model(:,:,60), anatomical_model(:,:,75), anatomical_model(:,:,90), anatomical_model(:,:,115)], []);
hcb = colorbar;  colormap(jet);
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);

%plot2svg('t1_anatomical_models.svg', 1);


%% 2. Anatomical model with removed labels other than WM, GM and CSF labels
anatomical_model2 = anatomical_model;
anatomical_model2(anatomical_model2 > 3) = 0;

figure(3), imshow([anatomical_model2(:,:,60), anatomical_model2(:,:,75), anatomical_model2(:,:,90), anatomical_model2(:,:,115)], []);
hcb = colorbar;  colormap(jet);
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);


%plot2svg('t1_anatomical_models.svg', 1);



%% 3. Only one single label

% select only the label associated with gray matter
% (see the documentation of the function openAnatomicalModel)
anatomical_model3 = anatomical_model;
anatomical_model3(anatomical_model3 ~= 2) = 0; % set all labels other than ==2 to zero

figure(4), imshow([anatomical_model3(:,:,60), anatomical_model3(:,:,75), anatomical_model3(:,:,90), anatomical_model3(:,:,115)], []);
hcb = colorbar;  colormap(jet);
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);


%plot2svg('t1_anatomical_models.svg', 1);


