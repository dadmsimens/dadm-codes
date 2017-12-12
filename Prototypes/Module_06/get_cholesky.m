function tensor_triangular_vector_output = get_cholesky( ...
    tensor_traingular_vector_input )
%GET_CHOLESKY Summary of this function goes here
%   Detailed explanation goes here

% Based on Eq. 5 and 6 from "A unifying theoretical..."

ln_measurement = tensor_traingular_vector_input(1);
tensor_estimate = tensor_traingular_vector_input(2:end);

Dxx = tensor_estimate(1)^2;
Dyy = tensor_estimate(2)^2 + tensor_estimate(4)^2;
Dzz = tensor_estimate(3)^2 + tensor_estimate(5)^2 + tensor_estimate(6)^2;
Dxy = tensor_estimate(1) * tensor_estimate(4);
Dyz = tensor_estimate(2)*tensor_estimate(5) + tensor_estimate(4)*tensor_estimate(6);
Dxz = tensor_estimate(1) * tensor_estimate(6);

tensor_triangular_vector_output = [ln_measurement, Dxx, Dyy, Dzz, Dxy, Dyz, Dxz]';

end

