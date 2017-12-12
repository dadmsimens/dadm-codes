function FA_image = get_FA( dwi )
%GET_FA Summary of this function goes here
%   Detailed explanation goes here

eig_variance = get_eig_variance(dwi);
sum_squared = sum_squares(dwi.eig_image);

FA_image = zeros(size(dwi.eig_image,1), size(dwi.eig_image,2));
FA_image(dwi.mask) = sqrt(3/2) * sqrt(...
    eig_variance(dwi.mask) ./ sum_squared(dwi.mask) );

end

function output = sum_squares( eig_image )

output = eig_image(:,:,1).^2 + eig_image(:,:,2).^2 + eig_image(:,:,3).^2;

end