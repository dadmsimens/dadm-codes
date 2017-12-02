function [ MD_image ] = get_MD( eig_image )
%GET_MD Summary of this function goes here
%   Detailed explanation goes here

MD_image = mean(eig_image,3);

end

