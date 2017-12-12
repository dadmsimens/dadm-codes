function tensor = get_tensor_from_vector( tensor_triangular_vector )
%GET_TENSOR_FROM_VECTOR Summary of this function goes here
%   Detailed explanation goes here

tensor = zeros(3,3);

% x-row
tensor(1,1) = tensor_triangular_vector(1);
tensor(1,2) = tensor_triangular_vector(4);
tensor(1,3) = tensor_triangular_vector(6);

% y-row
tensor(2,1) = tensor_triangular_vector(4);
tensor(2,2) = tensor_triangular_vector(2);
tensor(2,3) = tensor_triangular_vector(5);

% z-row
tensor(3,1) = tensor_triangular_vector(6);
tensor(3,2) = tensor_triangular_vector(5);
tensor(3,3) = tensor_triangular_vector(3);

end

