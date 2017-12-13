% Open BrainWeb dataset
%
% Tomasz Pieciak
% 1) ETS Ingenieros de Telecomunicacion, Universidad de Valladolid, Spain
% 2) AGH University of Science and Technology, Krakow, Poland
%
% e-mail: pieciak@agh.edu.pl
% www: http://home.agh.edu.pl/pieciak/
%
% INPUTS
%   filename - filename to open
%   xspace, yspace, zspace - dataset size in x, y and z dimension, respectively
%   resize_volume - resize the volume to 256x256? (1 - yes; 0 - no)
%
% OUTPUTS
%   dataset_rotated - single dataset (3D volume)

function [dataset_rotated] = openBrainWebData(filename_data, xspace, yspace, zspace, resize_volume)
%przykladowe wywolanie
%dataset_T1 = openBrainWebData('T1/t1_icbm_normal_1mm_pn0_rf0.rawb', 181, 217, 181, 1);


% MRI data
fid = fopen(filename_data, 'r');
[data, count] = fread(fid, 'uint8'); 
fclose(fid);

% reshaping
dataset = reshape(data, xspace, yspace, zspace);

% rotating the resizing the data
if(resize_volume == 1)
    dataset_rotated = zeros(256, 256, size(dataset, 3));

    for i=1:size(dataset, 3)
        dataset_rotated(:, :, i) = padarray(padarray(imrotate(dataset(:, :, i), 90), [19, 37], 0, 'pre'), [20, 38], 0, 'post');    
    end          
    
else
    dataset_rotated = zeros(size(dataset, 2), size(dataset, 1), size(dataset, 3));

    for i=1:size(dataset, 3)
        dataset_rotated(:, :, i) = imrotate(dataset(:, :, i), 90);    
    end             
end