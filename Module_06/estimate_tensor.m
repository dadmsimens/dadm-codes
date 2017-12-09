function tensor_image = estimate_tensor( dwi, SOLVER, FIX )
%ESTIMATE_TENSOR Summary of this function goes here
%   Detailed explanation goes here

% Based on:
% "A unifying theoretical and algorithmic framework for least
% squares methods of estimation in diffusion tensor imaging"

% Find the design matrix
% Ref: Eq.8 from "Estimation of the Effective Self-Diffusion Tensor
% from the NMR Spin-Echo." and Eq.4 from the one mentioned above.
W = get_design_matrix(dwi.bvals, dwi.bvecs);

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
        options = 'WLS';
    case 'NLS'
        options = 'NLS';
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
        estimate = solve_wls(measurement, W);
    case 'NLS'
        error('NLS is not implemented yet.');
    otherwise
        error('Unrecognized SOLVER type.');
end

% Solve for Cholesky parametrization so that D is positive definite
if strcmp(FIX, 'CHOLESKY')
    estimate = get_cholesky(estimate);
end

% ignore the estimate of ln(S0)
estimate = estimate(2:end);

end

function estimate = solve_matlab ( measurement, W, options, FIX )

% Initial guess for NLS
% should be WLS solution 
tensor_0 = solve_wls ( measurement, W );
if strcmp(FIX, 'CHOLESKY')
    tensor_0 = get_cholesky(tensor_0);
end

% Matlab implementation - NLS        
error_fun = @(tensor)(measurement - exp(W*tensor));
estimate = lsqnonlin(error_fun, tensor_0, [], [], options);

end

function estimate_wls = solve_wls ( measurement, W )

weights = eye(size(measurement,1)).*repmat(measurement,[1,size(measurement,1)]);
estimate_wls = pinv(W'*weights^2*W) * (weights*W)'*weights*log(measurement);

end