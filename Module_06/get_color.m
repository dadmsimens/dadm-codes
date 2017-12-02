function color_image = get_color( tensor_image, FIX)
%GET_COLOR Summary of this function goes here
%   Detailed explanation goes here

color_image = zeros(size(tensor_image,1), size(tensor_image,2), 3);

for id_x = 1:size(tensor_image,1)
    for id_y = 1:size(tensor_image,2)
        
        tensor = get_tensor_from_vector(tensor_image(id_x, id_y, :));
        [eig_values, eig_vecs] = eig(tensor);
        
        if strcmp(FIX, 'ABS')
            eig_values = abs(eig_values);
        end
        
        [~, principal_idx] = max(eig_values);
        color_image(id_x, id_y,:) = eig_values(principal_idx) * eig_vecs(:,principal_idx);
        
    end
end

end
