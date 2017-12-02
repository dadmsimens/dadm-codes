function plot_tensor( tensor_image )
%PLOT_TENSOR Summary of this function goes here
%   Detailed explanation goes here

figure;

% x-row
subplot(3,3,1); imshow(tensor_image(:,:,1),[]); title('Dxx');
subplot(3,3,2); imshow(tensor_image(:,:,4),[]); title('Dxy');
subplot(3,3,3); imshow(tensor_image(:,:,6),[]); title('Dxz');

% y-row
subplot(3,3,4); imshow(tensor_image(:,:,4),[]); title('Dyx');
subplot(3,3,5); imshow(tensor_image(:,:,2),[]); title('Dyy');
subplot(3,3,6); imshow(tensor_image(:,:,5),[]); title('Dyz');

% z-row
subplot(3,3,7); imshow(tensor_image(:,:,6),[]); title('Dzx');
subplot(3,3,8); imshow(tensor_image(:,:,5),[]); title('Dzy');
subplot(3,3,9); imshow(tensor_image(:,:,3),[]); title('Dzz');

suptitle('Diffusion Tensor Estimate Images');

end

