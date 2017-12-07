
rng default

close all
clear all

EPSILON = 1e-8;
FIX = 'ABS';
SOLVER = 'MATLAB';

%% Load reconstructed and filtered data

filenameIndex = 40;

load(sprintf('data/rec_%d.mat', filenameIndex));
load('data/mask.mat');
dwi.mask = mask;

% important: equations assume that data is in signal units, not pixels
% DWI must thus be non-zero
dwi.data = normalize_data(dwi, EPSILON);

% check if bvecs values are of unit length
eval_bvecs(dwi);

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
dwi.tensor_image = estimate_tensor(dwi, SOLVER, FIX, EPSILON);


%% Plot results in a 3x3 matrix
plot_tensor(dwi);


%% Obtain tensor eigenvalues
dwi.eig_image = estimate_eig(dwi, FIX);


%% Plot an eigenvalue image
plot_eig(dwi);


%% Biomarkers
plot_biomarker(dwi,'all');


%% Get tensor image in color
dwi.color_image = get_color(dwi, FIX);


%% Plot color image
plot_color(dwi, 'all');

