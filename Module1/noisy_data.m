% Function for preparing data with noise
% INPUTS: 
%             image - the size of the image1 defines the size of noise,
%             nc - number of coils,
%             maps - sensitivity maps for each coil,
%             std=const.(chosen standard deviation),
%             rho - correlation between channels.        
%
% OUTPUTS:
%             noise - random noise generated for each coil,
%             data_simulated - data with additive noise.
%
% LATER: work on adding another kind of noise to the image1 (!)

function [data_simulated, noise, noiseless_data, maps] = noisy_data(image, nc, maps, std, rho)
% normally distributed noise in each coil in x-space domain 
% noise = generate_noise(std, image1, n_coils, rho); % commented by TP
[Mx, My] = size(image);

% noiseless data
noiseless_data = repmat(image, [1, 1, nc]);

% noise generation
noise = randn([size(image), nc]) + 1i.*randn([size(image), nc]);

% no correlation between receiver coils
if(rho == 0)  
    data_simulated =  noiseless_data .* maps + std.*noise;    
else
    % covariance matrix
    cov_matrix = std.^2.*(eye(nc) + rho.*(1 - eye(nc)));
    
    % eigendecomposition
    [V, D] = eig(cov_matrix);
    
    % correlating filter
    W = V*sqrt(D);

    % correlate the noise
    noise_correlated = complex(zeros(size(noise)), 0);
        
   	for k=1:Mx
        for l=1:My
            noise_correlated(l, k, :) = W*squeeze(noise(l, k, :));
        end
   	end        

    % data simulated in x-space in each receiver coil    
    data_simulated = noiseless_data .* maps + noise_correlated;    
end

end

