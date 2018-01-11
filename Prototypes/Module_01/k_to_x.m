% Function creating data in x-space 
% INPUTS: data in k-space
%         n_coils - number of coils
%
% OUTPUTS:
%         data in x-space
function x_space_subsampled = k_to_x(k_space_subsampled, n_coils)
x_space_subsampled = zeros(size(k_space_subsampled));
for c=1:n_coils  
    x_space_subsampled(:,:,c) = ifft2(k_space_subsampled(:,:,c));  
end
end