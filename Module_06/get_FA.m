function FA_image = get_FA( eig_image )
%GET_FA Summary of this function goes here
%   Detailed explanation goes here

FA_image = sqrt(3/2) * sqrt(get_eig_variance(eig_image) ./ sum_squares( eig_image ));

end

function output = sum_squares( eig_image )

output = eig_image(:,:,1).^2 + eig_image(:,:,2).^2 + eig_image(:,:,3).^2;

end