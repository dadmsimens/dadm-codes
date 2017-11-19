%% Load synthetic data (the data from PhD thesis)
clear all; close all;

load('./DATA/FromPhDThesis/DATA_synthetic_brain.mat');

% slices at different vertical positions (!!!)
I = I_T1;  % T1 data
% I = I_T2;  % T2 data
%I = I_PD;  % PD data
% I = I_T1_INU;  % T1 data with INU=40%

% mask calculation
threshold_lvl = 10;
I_mask = imfill(I > threshold_lvl, 'holes');

% visualization
text_size = 20;

% #1
figure(1), imshow(I_mask,[]);

% #2
figure(2), imshow(I, []);
hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);

% #3
figure(3), imshow([I_T1, I_T2, I_PD, I_T1_INU], []);
hcb = colorbar; caxis([0, 255]);  set(hcb,'YTick', 0:50:255); 
set(gca, 'FontSize', text_size);  set(get(gca,'xlabel'), 'FontSize', text_size);  set(get(gca,'ylabel'), 'FontSize', text_size);  set(get(gca,'title'), 'FontSize', text_size);




