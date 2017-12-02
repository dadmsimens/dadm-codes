function VR_image = get_VR( eig_image )
%GET_VR Summary of this function goes here
%   Detailed explanation goes here

MD = get_MD(eig_image);

VR_image = eig_image(:,:,1).*eig_image(:,:,2).*eig_image(:,:,3) ./ (MD.^3);

end

