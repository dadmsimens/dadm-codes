% Open anatomical model for BrainWeb dataset (valid only for 1mm)
%
% Created: 14/10/2016
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
%   model - anatomical model for BrainWeb data (3D volume):
%           0=Background, 1=CSF, 2=Grey Matter, 3=White Matter, 4=Fat, 
%           5=Muscle/Skin, 6=Skin, 7=Skull, 8=Glial Matter, 9=Connective
% USAGE


function [model_rotated] = openAnatomicalModel(filename_data, xpace, yspace, zspace, resize_volume)

% MRI data
fid = fopen(filename_data, 'r');
[data, count] = fread(fid, 'uint8'); 
fclose(fid);

% reshaping
model = reshape(data, xpace, yspace, zspace);

% rotating the resizing the data
if(resize_volume == 1)
    model_rotated = zeros(256, 256, size(model, 3));

    for i=1:size(model, 3)
        model_rotated(:, :, i) = padarray(padarray(imrotate(model(:, :, i), 90), [19, 37], 0, 'pre'), [20, 38], 0, 'post');    
    end          
    
else
    model_rotated = zeros(size(model, 2), size(model, 1), size(model, 3));

    for i=1:size(model, 3)
        model_rotated(:, :, i) = imrotate(model(:, :, i), 90);    
    end             
end

