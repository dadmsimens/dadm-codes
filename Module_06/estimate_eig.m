function eig_image = estimate_eig( tensor_image, FIX )
%ESTIMATE_EIG Summary of this function goes here
%   Detailed explanation goes here

% reconstruct the entire tensor from vector - temp function
% should be direct calculation, without reconstructing the tensor first
eig_image = zeros(size(tensor_image,1), size(tensor_image,2), 3);

for id_x = 1:size(tensor_image,1)
    for id_y = 1:size(tensor_image,2)
        
        tensor = get_tensor_from_vector(tensor_image(id_x, id_y, :));
        eig_image(id_x,id_y,:) = eig(tensor);
        
        if strcmp(FIX, 'ABS')
            eig_image(id_x,id_y,:) = abs(eig_image(id_x,id_y,:));
        end
        
    end
end

end

