function plot_eig( dwi )
%PLOT_EIG Summary of this function goes here
%   Detailed explanation goes here

figure;

subplot(1,3,1); imshow(dwi.eig_image(:,:,1),[]); title('\lambda_{1}');
subplot(1,3,2); imshow(dwi.eig_image(:,:,2),[]); title('\lambda_{2}');
subplot(1,3,3); imshow(dwi.eig_image(:,:,3),[]); title('\lambda_{3}');

suptitle('Diffusion Tensor Estimate Eigenvalue Images');

end

