function eig_image = estimate_eig( dwi, FIX )
%ESTIMATE_EIG Summary of this function goes here
%   Detailed explanation goes here

% reconstruct the entire tensor from vector - temp function
% should be direct calculation, without reconstructing the tensor first
eig_image = zeros(size(dwi.tensor_image,1), size(dwi.tensor_image,2), 3);

for id_x = 1:size(dwi.tensor_image,1)
    for id_y = 1:size(dwi.tensor_image,2)
        
        if dwi.mask(id_x, id_y) == 1
            tensor = get_tensor_from_vector(dwi.tensor_image(id_x, id_y, :));
            eig_image(id_x,id_y,:) = eig(tensor);

            switch(FIX)
                case 'ABS'
                    eig_image(id_x,id_y,:) = abs(eig_image(id_x,id_y,:));
                case 'ZERO'
                    eig_image(id_x,id_y,eig_image(id_x,id_y,:)<0) = 0;
            end
            
        end
        
    end
end

end

