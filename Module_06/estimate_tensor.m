function tensor_image = estimate_tensor( dwi, SOLVER, FIX )
%ESTIMATE_TENSOR Summary of this function goes here
%   Detailed explanation goes here

% Based on:
% "A unifying theoretical and algorithmic framework for least
% squares methods of estimation in diffusion tensor imaging"

%% Set MFN parameters
MAX_ITER = 10;
NLS_EPSILON = 1e-5;
GRADIENT_EPSILON = 1e-5;


%% Body
% Find the design matrix
% Ref: Eq.8 from "Estimation of the Effective Self-Diffusion Tensor
% from the NMR Spin-Echo." and Eq.4 from the one mentioned above.
W = get_design_matrix(dwi.bvals, dwi.bvecs);
LAMBDA_MATRIX = zeros(size(W,2));

% Initialize tensor image
tensor_image = zeros(size(dwi.data,1), size(dwi.data,2), 6);

% SOLVER options
switch(SOLVER)
    case 'MATLAB'
        if ~license('test', 'optimization_toolbox')
            error('MATLAB solver requires Optimization Toolbox license.');
        end
        options = optimoptions('lsqnonlin', 'Algorithm', 'levenberg-marquardt',...
            'Display', 'off');
    case 'WLS'
        options = struct('max_iter', MAX_ITER, ...
            'nls_epsilon', NLS_EPSILON, ...
            'gradient_epsilon', GRADIENT_EPSILON, ...
            'lambda_matrix', LAMBDA_MATRIX);
    case 'NLS'
        options = struct('max_iter', MAX_ITER, ...
            'nls_epsilon', NLS_EPSILON, ...
            'gradient_epsilon', GRADIENT_EPSILON, ...
            'lambda_matrix', LAMBDA_MATRIX);
end

% Loop over voxels
for id_x = 1:size(dwi.data,1)
    for id_y = 1:size(dwi.data,2)
        
        if dwi.mask(id_x,id_y) == 1
            % Get sample pixel measurement
            measurement = squeeze(dwi.data(id_x,id_y,:));

            % Solve
            tensor_image(id_x, id_y, :) = solve(measurement, W, options,...
                SOLVER, FIX);    
        end

    end
    fprintf('Progress: %.2f%%\n', 100*id_x/size(dwi.data,1))
end

end

function estimate = solve( measurement, W, options, SOLVER, FIX )

switch(SOLVER)
    case 'MATLAB'
        estimate = solve_matlab(measurement, W, options, FIX);
    case 'WLS'
        estimate = solve_wls(measurement, W, options, FIX);
    case 'NLS'
        estimate = solve_mfn(measurement, W, options, FIX, 'NLS');
    otherwise
        error('Unrecognized SOLVER type.');
end

% ignore the estimate of ln(S0)
estimate = estimate(2:end);

end

function estimate_matlab = solve_matlab ( measurement, W, options, FIX )

% Initial guess for NLS
% should be WLS solution 
estimate = solve_wls ( measurement, W );

% Matlab implementation - NLS        
error_fun = @(tensor)(measurement - exp(W*tensor));
estimate_matlab = lsqnonlin(error_fun, estimate, [], [], options);

end

function estimate_wls = solve_wls ( measurement, W, options, FIX )

if nargin < 3
    options = [];
    FIX = '';
end

% use MFN to solve for cholesky parametrization
if strcmp(FIX, 'CHOLESKY')
    estimate_wls = solve_mfn(measurement, W, options, FIX, 'WLS');
    
else
    weights = get_wls_weights(measurement, W);

    weights = eye(size(weights,1)).*repmat(weights,[1,size(weights,1)]);
    estimate_wls = pinv(W'*weights^2*W) * (weights*W)'*weights*log(measurement);
end

end

function estimate_mfn = solve_mfn ( measurement, W, options, FIX, SOLVER)

%% Parameters
lambda = 0;
MAX_ITER = options.max_iter;
NLS_EPSILON = options.nls_epsilon;
GRADIENT_EPSILON = options.gradient_epsilon;
LAMBDA_MATRIX = options.lambda_matrix;
hessian_flag = 1;

%% Get proper function handles
switch(SOLVER)
    case 'NLS'
        get_hessian = @get_nls_hessian;
        get_gradient = @get_nls_gradient;
        get_error_value = @get_nls_error_value;
    case 'WLS'
        get_hessian = @get_wls_hessian;
        get_gradient = @get_wls_gradient;
        get_error_value = @get_wls_error_value;
end


%% Initialization
% Initial guess for MFN should be the unconstrained WLS solution 
estimate = solve_wls ( measurement, W );
error_old = get_error_value(measurement, W, estimate);


%% Iterate
for k = 1:MAX_ITER + 1
    
    if hessian_flag == 1
       hessian = get_hessian(measurement, W, estimate, FIX);
       hessian = hessian + lambda*LAMBDA_MATRIX;  % from MFN algorithm
       gradient = get_gradient(measurement, W, estimate, FIX);
       hessian_flag = 0;
    end
    delta = -pinv(hessian)*gradient;
    error_new = get_error_value(measurement, W, estimate+delta);
    
    % check for convergence
    if (abs(error_new-error_old) < NLS_EPSILON) || ...
            (-delta'*gradient >= 0 && -delta'*gradient < GRADIENT_EPSILON)
        
        if error_new < error_old
            estimate_mfn = estimate + delta;
        else
            estimate_mfn = estimate;
        end
        break
    end
    
    % check if current estimate achieves lower nls_error
    if error_new < error_old
        lambda = 0.1 * lambda;
        estimate = estimate + delta;
        hessian_flag = true;
        error_old = error_new;
        
    else
        % check if first iteration
        if lambda == 0
           lambda = 1e-4; 
        else
            lambda = 10 * lambda;
        end
        
    end
    
end

% check if iteration limit exceeded without convergence
if ~exist('estimate_nls', 'var')
    estimate_mfn = estimate;
end

% Solve for Cholesky parametrization so that D is a positive definite
if strcmp(FIX, 'CHOLESKY')
    estimate_mfn = get_cholesky(estimate_mfn);
end

end

function nls_error = get_nls_error_value ( measurement, W, estimate )

measurement_estimated = measurement - exp(W*estimate);

nls_error = 1/2 * (measurement_estimated)' * (measurement_estimated);

end

function wls_error = get_wls_error_value (measurement, W, estimate )

weights = get_wls_weights(measurement, W);

measurement_estimated  = weights .* (log(measurement) - W * estimate);

wls_error = 1/2 * (measurement_estimated)' * (measurement_estimated);

end

function nls_hessian = get_nls_hessian ( measurement, W, estimate, FIX )

if strcmp(FIX, 'CHOLESKY')
    J_matrix = get_cholesky_J_matrix(estimate);
    P_matrix = get_cholesky_P_matrix(W);
end

no_samples = size(measurement,1);

measurement = repmat(measurement, 1, no_samples) .* eye(no_samples);
measurement_estimated = repmat(exp(W*estimate), 1, no_samples) .* eye(no_samples);
nls_residual = measurement - measurement_estimated;

if strcmp(FIX, 'CHOLESKY')
    reduced_sum = zeros(7);
    for idx = 1:no_samples
        temp = nls_residual * measurement_estimated;
        reduced_sum = reduced_sum + temp(temp(:,idx)~=0, idx) * P_matrix(:,:,idx);
    end
    
    nls_hessian = J_matrix' * W' * ...
        (measurement_estimated - nls_residual*measurement_estimated) ...
        * W * J_matrix + reduced_sum;
else
    nls_hessian = W' * (measurement_estimated - nls_residual*measurement_estimated) * W;
end

end

function wls_hessian = get_wls_hessian ( measurement, W, estimate, FIX )

weights = get_wls_weights(measurement, W);

if strcmp(FIX, 'CHOLESKY')
    J_matrix = get_cholesky_J_matrix(estimate);
    P_matrix = get_cholesky_P_matrix(W);
end

no_samples = size(measurement,1);

if strcmp(FIX, 'CHOLESKY')
    reduced_sum = zeros(7);
    measurement_estimated  = weights.^2 .* (log(measurement) - W * estimate);
    for idx = 1:no_samples
        reduced_sum = reduced_sum + measurement_estimated(idx,1) * P_matrix(:,:,idx);
    end
    
    wls_hessian = J_matrix' * W' * (weights' * weights) ...
        * W * J_matrix + reduced_sum;
else
    wls_hessian = W' * (weights' * weights) * W;
end

end

function nls_gradient = get_nls_gradient ( measurement, W, estimate, FIX)

if strcmp(FIX, 'CHOLESKY')
    J_matrix = get_cholesky_J_matrix(estimate);
end

no_samples = size(measurement,1);

measurement_estimated = exp(W*estimate);
nls_residual = measurement - measurement_estimated;
measurement_estimated = repmat(measurement_estimated, 1, no_samples) .* eye(no_samples);

if strcmp(FIX, 'CHOLESKY')
    nls_gradient = -J_matrix'*(measurement_estimated*W)' * nls_residual;
else
    nls_gradient = -(measurement_estimated*W)' * nls_residual;
end

end

function wls_gradient = get_wls_gradient ( measurement, W, estimate, FIX)

weights = get_wls_weights(measurement, W);

if strcmp(FIX, 'CHOLESKY')
    J_matrix = get_cholesky_J_matrix(estimate);
end

if strcmp(FIX, 'CHOLESKY')
    wls_gradient = -J_matrix' * W' * (weights * weights') * ...
        (log(measurement) - W * estimate);
else
    wls_gradient = -W' * (weights * weights') * ...
        (log(measurement) - W * estimate);
end

end

function J_matrix = get_cholesky_J_matrix ( estimate )

J_matrix = zeros(7);

J_matrix(:,1) = [1, 0, 0, 0, 0, 0, 0];
J_matrix(:,2) = [0, 2*estimate(2), 0, 0, estimate(5), 0, estimate(7)];
J_matrix(:,3) = [0, 0, 2*estimate(3), 0, 0, estimate(6), 0];
J_matrix(:,4) = [0, 0, 0, 2*estimate(4), 0, 0 ,0];
J_matrix(:,5) = [0, 0, 2*estimate(5), 0, estimate(2), estimate(7), 0];
J_matrix(:,6) = [0, 0, 0, 2*estimate(6), 0, estimate(3), 0];
J_matrix(:,7) = [0, 0, 0, 2*estimate(7), 0, estimate(5), estimate(2)];

end

function P_matrix = get_cholesky_P_matrix ( W )

no_samples = size(W,1);
P_matrix = zeros(7,7,no_samples);

for idx = 1:no_samples
    P_matrix(:,1,idx) = [0, 0, 0, 0, 0, 0, 0,];
    P_matrix(:,2,idx) = [0, 2*W(idx,2), 0, 0, W(idx,5), 0, W(idx,7)];
    P_matrix(:,3,idx) = [0, 0, 2*W(idx,3), 0, 0, W(idx,6), 0];
    P_matrix(:,4,idx) = [0, 0, 0, 2*W(idx,4), 0, 0, 0];
    P_matrix(:,5,idx) = [0, W(idx,5), 0, 0, 2*W(idx,3), 0, W(idx,6)];
    P_matrix(:,6,idx) = [0, 0, W(idx,6), 0, 0, 2*W(idx,4), 0];
    P_matrix(:,7,idx) = [0, W(idx,7), 0, 0, W(idx,6), 0, 2*W(idx,4)];
end

P_matrix = -1 * P_matrix;

end

function weights = get_wls_weights ( measurement, W )

weights = measurement;

end