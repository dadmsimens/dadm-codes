function [ MD_image ] = get_MD( dwi )
%GET_MD Summary of this function goes here
%   Detailed explanation goes here

MD_image = mean(dwi.eig_image,3);

end

