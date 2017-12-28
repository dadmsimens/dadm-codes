%%
% Read image to be filtered.

I = imread('mozg.jpg');
I = I(:,:,1)
%%
figure(1)
imshow(I)
Iblur = imgaussfilt(I, 172);
%%
figure(2)
subplot(1,2,1)
imshow(I)
title('Original Image');
subplot(1,2,2)
imshow(Iblur)
title('Gaussian filtered image, \sigma = 172')
figure(3)
imhist(Iblur)
% BW = im2bw(I, 0.14)
% figure(4)
% imshow(BW)
I = I ./ Iblur;
figure(4)
imshow(I)

