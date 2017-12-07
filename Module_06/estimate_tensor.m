function tensor_image = estimate_tensor( dwi, SOLVER, FIX, EPSILON )
%ESTIMATE_TENSOR Summary of this function goes here
%   Detailed explanation goes here

% Based on:
% "A unifying theoretical and algorithmic framework for least
% squares methods of estimation in diffusion tensor imaging"

% Find reference image or their mean, if more than one
ref_idx = dwi.bvals == 0;
ref_image = mean(dwi.data(:,:,ref_idx),3);

% Find the design matrix
% Ref: Eq.8 from "Estimation of the Effective Self-Diffusion Tensor
% from the NMR Spin-Echo." and Eq.4 from the one mentioned above.
W = get_design_matrix(dwi.bvals(~ref_idx,:), dwi.bvecs(~ref_idx,:));

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
            % Get sample pixel attenuation
            sample_pixel = squeeze(dwi.data(id_x,id_y,~ref_idx));
            attenuation = log(sample_pixel/ref_image(id_x,id_y));

            % Solve
            tensor_image(id_x, id_y, :) = solve(attenuation, W, options,...
                SOLVER, FIX, EPSILON);    
        end

    end
    fprintf('Progress: %.2f%%\n', 100*id_x/size(dwi.data,1))
end

end

function estimate = solve( attenuation, W, options, SOLVER, FIX, EPSILON )

switch(SOLVER)
    case 'MATLAB'
        estimate = solve_matlab(attenuation, W, options);
    case 'WLS'
        error('WLS is not implemented yet.');
    case 'NLS'
        error('NLS is not implemented yet.');
    otherwise
        error('Unrecognized SOLVER type.');
end

% Solve for Cholesky parametrization so that D is positive definite
if strcmp(FIX, 'CHOLESKY')
    estimate = get_cholesky(estimate, EPSILON);
end

end

function estimate = solve_matlab ( attenuation, W, options )

% Initial guess for NLS
% should be WLS solution 
tensor_0 = ones(6,1);

% Matlab implementation - NLS        
error_fun = @(tensor)(attenuation - W*tensor);
estimate = lsqnonlin(error_fun, tensor_0, [], [], options);

end
