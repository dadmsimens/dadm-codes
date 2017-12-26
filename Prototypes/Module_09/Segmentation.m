close all;
clear all;
clc; 

fontSize = 12;

%% Load brain MRI data without skull

i = load('skullFreeImage.mat');
image = i.skullFreeImage;

% Displey the image 
figure;
subplot (1,3,1);
imshow(image,[]);
axis on;
caption = sprintf('Non-skull brain MRI Image');
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');

% Set up figure properties
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
set(gcf, 'Toolbar', 'none', 'Menu', 'none');
set(gcf, 'Name', 'Non-skull brain MRI image', 'NumberTitle', 'Off')

[rows, columns, nrColorChannel] = size(image);


%% Histogram of image and threshold selecting 

subplot(1,3,2:3);
% hist = histogram(image);
thresh = multithresh(image,3);                      % Histogram of non-zeros image
[pixelCounts, grayLevels] = imhist(uint8(image));
histo = histogram(image(image>=thresh(1)));

% Set histogram properties
lastGrayLevel = find(pixelCounts>0, 1, 'last');
xlim([0, lastGrayLevel]);                           % Set up axis range
grid on;
ax = gca;
ax.XTick = 0 : 50 : lastGrayLevel;                  % Set up tick marks every 50 gray levels.
title('Histogram of Non-Black Pixels', 'FontSize', fontSize, 'Interpreter', 'None');
xlabel('Gray Level', 'FontSize', fontSize);
ylabel('Pixel Counts', 'FontSize', fontSize);


%% Segmentation by thresholds

imCerebrospinal = zeros(size(image));
imGrayMatter = zeros(size(image));
imWhiteMatter = zeros(size(image));

for i=1:rows
    for j=1:columns
        if image(i,j) > thresh(1) && image(i,j) < thresh(2)
            imCerebrospinal(i,j) = 0.33;                     % P�yn m�zgowo-rdzeniowy
        elseif image(i,j) > thresh(2) && image(i,j) < thresh(3)
            imGrayMatter(i,j) = 0.66;                   % Istota szara
        elseif image(i,j) > thresh(3)
            imWhiteMatter(i,j) = 1;                     % Istota bia�a
        end
    end
end

segmentedBain = imCerebrospinal + imGrayMatter + imWhiteMatter;

% Set color for segmented elements of brain

% colorBackground = uisetcolor([0 0 0], 'Background');                % t�o
% colorWhiteMatter = uisetcolor([1 1 1], 'White Matter ');            % istota bia�a
% colorGrayMatter = uisetcolor([0.8 0.8 0.8], 'Gray Matter');         % istota szara
% colorCerebrum = uisetcolor([0.302 0.7451 0.9333], 'Cerebrum');      % p�yn m�zgowo-rdzeniowy

figure;
subplot(1,3,1)
imshow(imCerebrospinal,[]);
subplot(1,3,2)
imshow(imWhiteMatter,[]);
subplot(1,3,3)
imshow(imGrayMatter,[]);

%  Set up figure properties
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
set(gcf, 'Toolbar', 'none', 'Menu', 'none');
set(gcf, 'Name', 'Segmentation', 'NumberTitle', 'Off');

map_imBackground = [0 0 0];
map_imCerebrospinal = [0.302 0.7451 0.9333];
map_imWhiteMatter = [1 1 1];
map_imGrayMatter = [0.8 0.8 0.8];

figure;
imshow(segmentedBain,[]); hold on;
map = [map_imBackground; map_imCerebrospinal; map_imGrayMatter; map_imWhiteMatter];
colormap(map);

%% Saving segmented image 

save('Cerebrospinal.mat','imCerebrospinal');
save('WhiteMatter.mat','imWhiteMatter');
save('GrayMatter.mat','imGrayMatter');
save('SegmentedBrain.mat','segmentedBain');

%% 
% 
% grayLevels
% pixelCounts
% thresh

image_data = zeros(size(histo.Data));
j=1;

for i = 1:19936
    
   if thresh(1) == histo.Data(i)
       ind(j) = i;
       j = j+1;
   end
   
end