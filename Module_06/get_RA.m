function RA_image = get_RA( dwi )
%GET_RA Summary of this function goes here
%   Detailed explanation goes here

MD = get_MD(dwi);

eig_variance = get_eig_variance(dwi);

RA_image = zeros(size(MD));
RA_image(dwi.mask) = sqrt(eig_variance(dwi.mask) ./ (3*MD(dwi.mask)));

end