function tensor_triangular_vector_output = get_cholesky( ...
    tensor_triangular_vector_input, EPSILON )
%GET_CHOLESKY Summary of this function goes here
%   Detailed explanation goes here

% Based on Eq. 5 and 6 from "A unifying theoretical..."

% for estimates bounded by EPSILON assume that value is equal to zero
tensor_triangular_vector_input(abs(tensor_triangular_vector_input) < EPSILON) = 0;

cholesky_matrix = zeros(3,3);

p2 = sqrt(tensor_triangular_vector_input(1)) + EPSILON;
p5 = tensor_triangular_vector_input(4) / p2 + EPSILON;
p3 = sqrt(tensor_triangular_vector_input(2) - p5^2) + EPSILON;
p7 = tensor_triangular_vector_input(6) / p2 + EPSILON;
p6 = (tensor_triangular_vector_input(5) - p5*p7) / p3 + EPSILON;
p4 = sqrt(tensor_triangular_vector_input(3) - p6^2 - p7^2) + EPSILON;

cholesky_matrix(1,:) = [p2, p5, p7];
cholesky_matrix(2,:) = [0, p3, p6]; 
cholesky_matrix(3,:) = [0, 0, p4];

tensor = real(cholesky_matrix' * cholesky_matrix);

tensor_triangular_vector_output = [tensor(1,1), tensor(2,2), tensor(3,3), ...
    tensor(1,2), tensor(2,3), tensor(1,3)];

end

