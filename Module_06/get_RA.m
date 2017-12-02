function RA_image = get_RA( eig_image )
%GET_RA Summary of this function goes here
%   Detailed explanation goes here

MD = get_MD(eig_image);

RA_image = sqrt(get_eig_variance(eig_image) ./ (3*MD));

end