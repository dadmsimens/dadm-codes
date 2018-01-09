function image = singleImage(folder, fileName,pitchNumber)

fullFileName = fullfile(folder,fileName);

% Check if the file exist
if ~exist(fullFileName, 'file')
    fullFileNameOnSearchPath = fileName;    % No path
    if ~exist(fullFileNameOnSearchPath, 'file')
        % Still didn't find the image data. Alert user.
        errorMessage = sprintf('Error: %s does not exist in the search path folder.', fullFileName);
        uiwait(warndlg(errorMessage));
        return;
    end
end

% Read the image data 

BrainImage = load(fullFileName);        % loading image in .mat fortma if you have
                                        % in other way, use loadminc
                                        % function from the first
                                        % section
image = BrainImage.BrainMRIData(:,:,pitchNumber);% one test image

% Get the dimensions of the image
% number of color channels should be 1
[rows, columns, colorChannelsNumber] = size(image);
% SizeInformation = [rows, columns, colorChannelsNumber];

if colorChannelsNumber > 1
    image = image (:,:,2);               % if it's color image, take only the green channel                       
end


%% U¿yj zamiast funkcji:

% % % fullFileName = fullfile(folder,fileName);
% % % 
% % % % Check if the file exist
% % % if ~exist(fullFileName, 'file')
% % %     fullFileNameOnSearchPath = fileName;    % No path
% % %     if ~exist(fullFileNameOnSearchPath, 'file')
% % %         % Still didn't find the image data. Alert user.
% % %         errorMessage = sprintf('Error: %s does not exist in the search path folder.', fullFileName);
% % %         uiwait(warndlg(errorMessage));
% % %         return;
% % %     end
% % % end
% % % 
% % % % Read the image data 
% % % 
% % % BrainImage = load(fullFileName);        % loading image in .mat fortma if you have
% % %                                         % in other way, use loadminc
% % %                                         % function from the first
% % %                                         % section
% % % image = BrainImage.BrainMRIData(:,:,90);% one test image
% % % 
% % % % Get the dimensions of the image
% % % % number of color channels should be 1
% % % [rows, columns, colorChannelsNumber] = size(image);
% % % 
% % % if colorChannelsNumber > 1
% % %     image = image (:,:,2);               % if it's color image, take only the green channel                       
% % % end
