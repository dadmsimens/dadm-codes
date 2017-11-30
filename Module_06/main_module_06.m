
close all


%% Load reconstructed and filtered data

filenameIndex = 40;

load(sprintf('data/rec_%d.mat', filenameIndex));


%% Eddy Current / motion correction

% TODO: ...


%% Magnetic Susceptibility correction

% TODO: ...


%% Skull Stripping

% TODO: from Module 8


%% Tensor estimation

% Find reference image or their mean, if more than one
ref_image = mean(dwi.data(:,:,dwi.bvals == 0),3);
