
rng default

close all
clear all

EPSILON = 1e-8;
FIX = 'ABS';
SOLVER = 'MATLAB';

%% Load reconstructed and filtered data

filenameIndex = 48;

load(sprintf('data/rec_%d.mat', filenameIndex));

% important: equations assume that data is in signal units, not pixels
% DWI must thus be non-zero
dwi.data = normalize_data(dwi.data, EPSILON);

% check if bvecs values are of unit length
dwi.bvecs = eval_bvecs(dwi.bvecs, dwi.bvals);

% normalize bvals units from header file
% TODO: ...


%% Eddy Current / motion correction
% TODO: ...


%% Magnetic Susceptibility correction
% TODO: ...


%% Skull Stripping
% TODO: from Module 8
% Tensor image should be estimated only from brain data.


%% Tensor estimation
tensor_image = estimate_tensor(dwi, SOLVER, FIX, EPSILON);


%% Plot results in a 3x3 matrix
plot_tensor(tensor_image);


%% Obtain tensor eigenvalues
eig_image = estimate_eig(tensor_image, FIX);


%% Plot an eigenvalue image
plot_eig(eig_image);


%% Biomarkers
plot_biomarker(eig_image,'all');


%% Get tensor image in color
color_image = get_color(tensor_image, FIX);


%% Plot color image
plot_color(color_image, 'all');

