function eig_variance = get_eig_variance( dwi )
%GET_EIG_VARIANCE Summary of this function goes here
%   Detailed explanation goes here

MD = get_MD(dwi);

eig_variance = diff_squared(dwi.eig_image,1,MD) + ...
    diff_squared(dwi.eig_image,2,MD) + ...
    diff_squared(dwi.eig_image,3,MD);

end

function output = diff_squared( input, idx, MD)

output = (input(:,:,idx) - MD) .^ 2;

end
