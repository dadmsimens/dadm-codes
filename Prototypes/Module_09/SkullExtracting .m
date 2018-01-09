close all;
clear all;
clc;


%% Load image data in .mnc format and save as .mat file

% BrainMRIData = loadminc('T1_brain.mnc');
% save('Brain_MRI_Image_Data.mat', 'BrainMRIData');

%% Choose a single image by pitch

fileName = ('Brain_MRI_Image_Data.mat');    % loading file name
folder = ('ImageData');
pitchNumber = 90;                           % Choose single image

image = singleImage(folder, fileName, pitchNumber);


%% Display image and image without the skull 

thresholdValue = 34; 
skullFreeImage = ExtractSkull(image, thresholdValue);
save('skullFreeImage.mat','skullFreeImage')

% lastGrayLeve