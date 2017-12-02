function eig_variance = get_eig_variance( eig_image )
%GET_EIG_VARIANCE Summary of this function goes here
%   Detailed explanation goes here

MD = get_MD(eig_image);

eig_variance = diff_squared(eig_image,1,MD) + ...
    diff_squared(eig_image,2,MD) + ...
    diff_squared(eig_image,3,MD);

end

function output = diff_squared( input, idx, MD)

output = (input(:,:,idx) - MD) .^ 2;

end
