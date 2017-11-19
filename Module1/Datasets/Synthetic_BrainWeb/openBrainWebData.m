% Open BrainWeb dataset
%
% Created: 19/11/2014
% Revisited: 14/10/2016
% 
% Tomasz Pieciak
% 1) ETS Ingenieros de Telecomunicacion, Universidad de Valladolid, Spain
% 2) AGH University of Science and Technology, Krakow, Poland
%
% e-mail: pieciak@agh.edu.pl
% www: http://home.agh.edu.pl/pieciak/
%
% ARGUMENTS
%   filename - filename to open
%   xpace, yspace, zspace - dataset size in x, y and z dimension, respectively
%   resize_volume - resize the volume to 256x256? (1 - yes; 0 - no)
%
% FUNCTION RETURNS
%   dataset_rotated - single dataset (3D volume)
%
% USAGE


function [dataset_rotated] = openBrainWebData(filename_data, xpace, yspace, zspace, resize_volume)

% MRI data
fid = fopen(filename_data, 'r');
[data, count] = fread(fid, 'uint8'); 
fclose(fid);

% reshaping
dataset = reshape(data, xpace, yspace, zspace);

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

