%% Marker-controlled watershed segmentation
function brain = skull_watershed(I)
% Use the Sobel edge masks, imfilter, and some simple arithmetic to compute the gradient magnitude. 
hy = fspecial('sobel');
hx = hy';
Iy = imfilter(double(I), hy, 'replicate');
Ix = imfilter(double(I), hx, 'replicate');
gradmag = sqrt(Ix.^2 + Iy.^2);
figure
imshow(gradmag,[]), title('Gradient magnitude using of the Sobel edge mask')

%The watershed transform directly on the gradient magnitude
L = watershed(gradmag);
Lrgb = label2rgb(L);
figure, imshow(Lrgb), title('Watershed transform of gradient magnitude (Lrgb) - oversegmentation')
 
%Using morphological techniques called "opening-by-reconstruction" to "clean" up the image. 
se = strel('disk', 20);
Io = imopen(I, se);
figure
imshow(Io), title('Opening (Io)')

% Computing the opening-by-reconstruction using imerode and imreconstruct.
Ie = imerode(I, se);
Iobr = imreconstruct(Ie, I);
figure
imshow(Iobr), title('Opening-by-reconstruction (Iobr)')

% Using imdilate followed by imreconstruct
Iobrd = imdilate(Iobr, se);
Iobrcbr = imreconstruct(imcomplement(Iobrd), imcomplement(Iobr));
Iobrcbr = imcomplement(Iobrcbr);
figure
imshow(Iobrcbr), title('Opening-closing by reconstruction (Iobrcbr)')

%Calculating the regional maxima of Iobrcbr to obtain good foreground markers.
fgm = imregionalmax(Iobrcbr);
figure
imshow(fgm), title('Regional maxima of opening-closing by reconstruction (fgm)')

% Cleaning the edges of the marker blobs and then shrink them a bit - closing followed by an erosion.
se2 = strel(ones(5,5));
fgm2 = imclose(fgm, se2);
fgm3 = imerode(fgm2, se2);

% Using bwareaopen, which removes all blobs that have fewer than a certain number of pixels.
fgm4 = bwareaopen(fgm3, 20);
I3 = I;
I3(fgm4) = 255;
figure
imshow(I3)
title('Modified regional maxima superimposed on original image')

% Mark the background.
bw = imbinarize(I);
figure
imshow(bw), title('Binarized image') 

% Computing the watershed transform of the distance transform of binarized image and looking for the watershed ridge lines of the result.
D = bwdist(bw);
DL = watershed(D);
bgm = DL == 0;
figure
imshow(bgm), title('Watershed ridge lines')

% Modifing the gradient magnitude image to occur regional minima at foreground and background marker pixels.
gradmag2 = imimposemin(gradmag, bgm | fgm4);

% Computing the watershed-based segmentation.
L = watershed(gradmag2);

% Visualization
I4 = I;
I4(imdilate(L == 0, ones(3, 3)) | bgm | fgm4) = 0;
figure
imshow(I4)
title('Markers and object boundaries superimposed on original image')
Lrgb = label2rgb(L, 'jet', 'w', 'shuffle');
figure
imshow(Lrgb)
title('Colored watershed label matrix (Lrgb)')
figure
imshow(I)
hold on
himage = imshow(Lrgb);
himage.AlphaData = 0.3;
title('Lrgb superimposed transparently on original image')

% Setting up brain tissue on the output
boundaries = L == 2;
boundaries = imfill(boundaries,'holes');
figure
imshow(boundaries)
I(~boundaries) = 0;
brain = I;
end
