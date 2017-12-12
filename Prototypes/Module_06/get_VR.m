function VR_image = get_VR( dwi )
%GET_VR Summary of this function goes here
%   Detailed explanation goes here

MD = get_MD(dwi);

eig_image_subset_1 = dwi.eig_image(:,:,1);
eig_image_subset_2 = dwi.eig_image(:,:,2);
eig_image_subset_3 = dwi.eig_image(:,:,3);

VR_image = zeros(size(dwi.eig_image,1), size(dwi.eig_image,2));
VR_image(dwi.mask) = eig_image_subset_1(dwi.mask).*...
    eig_image_subset_2(dwi.mask).*eig_image_subset_3(dwi.mask) ./ (MD(dwi.mask).^3);

end

