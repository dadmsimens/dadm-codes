% Function for preparing data for reconstruction
% INPUTS: 
%             data_simulated - noisy data in each coil
%             n_coils - number of coils,
%             subsamp_rate - subsampling rate.
%
% OUTPUTS:
%         x_space_subsampled - data for reconstruction.
%
%LATER: work on subsampling scheme

function x_space_subsampled = data_preparation(data_simulated, nc, r)

% imitate data in k-space -> apply FFT to obtain raw data
k_space_data = x_to_k(data_simulated, nc);
 
% subsample data in k-space
k_space_subsampled = subsampling(k_space_data, r, nc);

% apply iDFT to each coil image to retrive data in x-space
x_space_subsampled = k_to_x(k_space_subsampled, nc);

end