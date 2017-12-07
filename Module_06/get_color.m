function color_image = get_color( dwi, FIX)
%GET_COLOR Summary of this function goes here
%   Detailed explanation goes here

color_image = zeros(size(dwi.tensor_image,1), size(dwi.tensor_image,2), 3);

for id_x = 1:size(dwi.tensor_image,1)
    for id_y = 1:size(dwi.tensor_image,2)
        
        if dwi.mask(id_x, id_y) == 1
            tensor = get_tensor_from_vector(dwi.tensor_image(id_x, id_y, :));
            [eig_values, eig_vecs] = eig(tensor);

            if strcmp(FIX, 'ABS')
                eig_values = abs(eig_values);
            end

            [~, principal_idx] = max(eig_values);
            % take abs of eigenvectors so that we preserve their main-axis
            % orientation, regardless of direction
            color_image(id_x, id_y,:) = eig_values(principal_idx) * abs(eig_vecs(:,principal_idx));
        end
    end
end

end
