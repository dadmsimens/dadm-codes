function skullFreeImage = ExtractSkull(image, thresholdValue)

fontSize = 12;

subplot(2,3,1);
imshow(image,[]);
axis on;
caption = sprintf('Original Brain MRI Image');
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');

pixelInfo = impixelinfo();

% Set up figure properties
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
% Get rid of tool bar and pulldown menus that are along top of figure.
set(gcf, 'Toolbar', 'none', 'Menu', 'none');
% Give a name to the title bar.
set(gcf, 'Name', 'Non-skull brain MRI image', 'NumberTitle', 'Off') 

% Make the pixel info status line be at the top left of the figure.
pixelInfo.Units = 'Normalized';
pixelInfo.Position = [0.01, 0.97, 0.08, 0.05];

% Change image value
image = 256*(image/(max(max(image))));

%% Display the image histogram
subplot (2,3,2:3);

histObj = histogram(image(image>=27));              % histogram for non-zero pixels
[pixelCounts, grayLevels] = imhist(uint8(image));
faceColor = [0, 60, 190]/255; % Our custom color - a bluish color.
bar(grayLevels, pixelCounts, 'BarWidth', 1, 'FaceColor', faceColor);
% Find the last gray level and set up the x axis to be that range.
lastGL = find(pixelCounts>0, 1, 'last');
xlim([0, lastGL]);
grid on;
% Set up tick marks every 50 gray levels.
ax = gca;
ax.XTick = 0 : 50 : lastGL;
title('Histogram of Non-Black Pixels', 'FontSize', fontSize, 'Interpreter', 'None', 'Color', faceColor);
xlabel('Gray Level', 'FontSize', fontSize);
ylabel('Pixel Counts', 'FontSize', fontSize);
drawnow;

%%
subplot(2,3,4:6);
skullFreeImage = skullDeley (image, thresholdValue);


%% U¿yj kodu zamiast funkcji:

% % % subplot(2,3,1);
% % % imshow(image,[]);
% % % axis on;
% % % caption = sprintf('Original Brain MRI Image');
% % % title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
% % % 
% % % pixelInfo = impixelinfo();
% % % 
% % % % Set up figure properties
% % % set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
% % % % Get rid of tool bar and pulldown menus that are along top of figure.
% % % set(gcf, 'Toolbar', 'none', 'Menu', 'none');
% % % % Give a name to the title bar.
% % % set(gcf, 'Name', 'Demo by ImageAnalyst', 'NumberTitle', 'Off') 
% % % 
% % % % Make the pixel info status line be at the top left of the figure.
% % % pixelInfo.Units = 'Normalized';
% % % pixelInfo.Position = [0.01, 0.97, 0.08, 0.05];
% % % 
% % % % Change image value
% % % image = 256*(image/(max(max(image))));
% % % 
% % % %% Display the image histogram
% % % subplot (2,3,2:3);
% % % 
% % % histObj = histogram(image(image>=27));              % histogram for non-zero pixels
% % % [pixelCounts, grayLevels] = imhist(uint8(image));
% % % faceColor = [0, 60, 190]/255; % Our custom color - a bluish color.
% % % bar(grayLevels, pixelCounts, 'BarWidth', 1, 'FaceColor', faceColor);
% % % % Find the last gray level and set up the x axis to be that range.
% % % lastGL = find(pixelCounts>0, 1, 'last');
% % % xlim([0, lastGL]);
% % % grid on;
% % % % Set up tick marks every 50 gray levels.
% % % ax = gca;
% % % ax.XTick = 0 : 50 : lastGL;
% % % title('Histogram of Non-Black Pixels', 'FontSize', fontSize, 'Interpreter', 'None', 'Color', faceColor);
% % % xlabel('Gray Level', 'FontSize', fontSize);
% % % ylabel('Pixel Counts', 'FontSize', fontSize);
% % % drawnow;

