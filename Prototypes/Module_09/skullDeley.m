function skullFreeImage = skullDeley (image, thresholdValue)

fontSize = 12;

%% Threshold the image to make a binary image.

% thresholdValue = 34;
binaryImage = image > thresholdValue;

% If it's a screenshot instead of an actual image, the background will be a big square, like with image sc4.
% So call imclearborder to remove that.
% If it's not a screenshow (which it should not be, you can skip this step).
binaryImage = imclearborder(binaryImage);
% Display the image.
% figure;
subplot(2, 3, 4);
imshow(binaryImage, []);
axis on;
caption = sprintf('Initial Binary Image\nThresholded at %d Gray Levels', thresholdValue);
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');

%% Extract the two largest blobs, which will either be the skull and brain, or the skull/brain (if they are connected) and small noise blob.

% Extract the two largest blobs, which will either be the skull and brain,
% or the skull/brain (if they are connected) and small noise blob.
binaryImage = bwareafilt(binaryImage, 2);		% Extract 2 largest blobs.
% Erode it a little with imdilate().
binaryImage = imopen(binaryImage, true(5));
% Now brain should be disconnected from skull, if it ever was.
% So extract the brain only - it's the largest blob.
binaryImage = bwareafilt(binaryImage, 1);		% Extract largest blob.
% Fill any holes in the brain.
binaryImage = imfill(binaryImage, 'holes');
% Dilate mask out a bit in case we've chopped out a little bit of brain.
binaryImage = imdilate(binaryImage, true(5));

% Display the final binary image.
subplot(2, 3, 5);
imshow(binaryImage, []);
axis on;
caption = sprintf('Final Binary Image\nof Skull Alone');
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');

%% Mask out the skull from the original gray scale image.

% Mask out the skull from the original gray scale image.
skullFreeImage = image; % Initialize
skullFreeImage(~binaryImage) = 0; % Mask out.
% Display the image.
subplot(2, 3, 6);
imshow(skullFreeImage, []);
axis on;
caption = sprintf('Gray Scale Image\nwith Skull Stripped Away');
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');




%% Bez u¿ycia funkcji - wklej kod:

% Zmieñ subplot obrazu wejsciowego na subplot(2,3,1) i histogramu na
% subplot(2,3,2:3)

% % % % %% Threshold the image to make a binary image.
% % % % 
% % % % thresholdValue = 34;
% % % % binaryImage = image > thresholdValue;
% % % % 
% % % % % If it's a screenshot instead of an actual image, the background will be a big square, like with image sc4.
% % % % % So call imclearborder to remove that.
% % % % % If it's not a screenshow (which it should not be, you can skip this step).
% % % % binaryImage = imclearborder(binaryImage);
% % % % % Display the image.
% % % % subplot(2, 3, 4);
% % % % imshow(binaryImage, []);
% % % % axis on;
% % % % caption = sprintf('Initial Binary Image\nThresholded at %d Gray Levels', thresholdValue);
% % % % title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
% % % % 
% % % % %% Extract the two largest blobs, which will either be the skull and brain, or the skull/brain (if they are connected) and small noise blob.
% % % % 
% % % % % Extract the two largest blobs, which will either be the skull and brain,
% % % % % or the skull/brain (if they are connected) and small noise blob.
% % % % binaryImage = bwareafilt(binaryImage, 2);		% Extract 2 largest blobs.
% % % % % Erode it a little with imdilate().
% % % % binaryImage = imopen(binaryImage, true(5));
% % % % % Now brain should be disconnected from skull, if it ever was.
% % % % % So extract the brain only - it's the largest blob.
% % % % binaryImage = bwareafilt(binaryImage, 1);		% Extract largest blob.
% % % % % Fill any holes in the brain.
% % % % binaryImage = imfill(binaryImage, 'holes');
% % % % % Dilate mask out a bit in case we've chopped out a little bit of brain.
% % % % binaryImage = imdilate(binaryImage, true(5));
% % % % 
% % % % % Display the final binary image.
% % % % subplot(2, 3, 5);
% % % % imshow(binaryImage, []);
% % % % axis on;
% % % % caption = sprintf('Final Binary Image\nof Skull Alone');
% % % % title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
% % % % 
% % % % %% Mask out the skull from the original gray scale image.
% % % % 
% % % % % Mask out the skull from the original gray scale image.
% % % % skullFreeImage = image; % Initialize
% % % % skullFreeImage(~binaryImage) = 0; % Mask out.
% % % % % Display the image.
% % % % subplot(2, 3, 6);
% % % % imshow(skullFreeImage, []);
% % % % axis on;
% % % % caption = sprintf('Gray Scale Image\nwith Skull Stripped Away');
% % % % title(caption, 'FontSize', fontSize, 'Interpreter', 'None');