
rng default

close all
clear all

FIX_ENUM = {'ZERO', 'ABS', 'CHOLESKY'};
SOLVER_ENUM = {'MATLAB', 'WLS', 'NLS'};

EPSILON = 1e-8;
FIX = FIX_ENUM{2};  % method error: ZERO > ABS >> CHOLESKY
SOLVER = SOLVER_ENUM{2};  % use 2 or 3

% TODO: take sqrt of tensor image after CHOLESKY?
% ^ right now the values are smaller than they should be

%% Load reconstructed and filtered data

filenameIndex = 40;

load(sprintf('data/rec_%d.mat', filenameIndex));
load('data/mask.mat');
dwi.mask = mask;

% important: equations assume that data is in signal units, not pixels
% DWI must thus be positive
dwi.data = normalize_data(dwi, EPSILON);

% check if bvecs values are of unit length
eval_bvecs(dwi);


%% Normalize bvals units from header file
% TODO: ...


%% Eddy Current / motion correction
% TODO: ...


%% Tensor estimation
dwi.tensor_image = estimate_tensor(dwi, SOLVER, FIX);


%% Plot results in a 3x3 matrix
plot_tensor(dwi);


%% Obtain tensor eigenvalues
% TODO: take square root if FIX=CHOLESKY? 
% Otherwise the values are really small
dwi.eig_image = estimate_eig(dwi, FIX);


%% Plot an eigenvalue image
plot_eig(dwi);


%% Biomarkers
plot_biomarker(dwi,'all');


%% Get tensor image in color
% dwi.color_image = get_color(dwi, FIX);


%% Plot color image
% plot_color(dwi, 'all');

