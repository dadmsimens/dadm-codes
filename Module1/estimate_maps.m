% Function
% INPUTS
% OUTPUTS
function estimated_maps = estimate_maps(data_simulated, data_sos, n_coils)

[size_x, size_y] = size(data_sos);
estimated_maps = zeros(size_x, size_y, n_coils);

for n=1:n_coils
    estimated_maps(:,:,n) = data_simulated(:,:,n)./data_sos;
end

end