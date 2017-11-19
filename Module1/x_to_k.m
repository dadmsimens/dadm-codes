% Function creating data in k-space
% INPUTS: data in x-space
%         n_coils - number of coils
%
% OUTPUTS:
%         data in k-space
function k_space_data = x_to_k(x_space_data, n_coils)

k_space_data = zeros(size(x_space_data));

for c=1:n_coils    
    k_space_data(:, :, c) = fftshift(fftshift(fft2(x_space_data(:, :, c)), 1), 2);
end

end