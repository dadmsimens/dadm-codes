function plot_color( dwi, type, figure_handle )
%PLOT_COLOR Summary of this function goes here
%   Detailed explanation goes here

% TODO: check if this is correct:
% red - x-axis
% green - y-axis
% blue - z-axis

if nargin < 3
    figure_handle = figure();
end

dwi.color_image = normalize_color(dwi);

switch(type)
    case 'one'
        color_image = less_channels(dwi, 1);
        imshow(color_image);
        title('Principal direction of diffusion - one channel');
    case 'two'
        color_image = less_channels(dwi, 2);
        imshow(color_image);
        title('Principal direction of diffusion - two channels');
    case 'three'
        imshow(dwi.color_image);
        title('Principal direction of diffusion - three channels');
    case 'all'
        subplot(1,3,1); plot_color(dwi, 'one', figure_handle);
        subplot(1,3,2); plot_color(dwi, 'two', figure_handle);
        subplot(1,3,3); plot_color(dwi, 'three', figure_handle);
end

end

function color_image = normalize_color ( dwi )

% normalize to 0-1 in each channel
minimum = repmat(min(min(min(dwi.color_image))),[size(dwi.color_image,1),size(dwi.color_image,2),3]);
maximum = repmat(max(max(max(dwi.color_image))),[size(dwi.color_image,1),size(dwi.color_image,2),3]);
color_image = (dwi.color_image - minimum) ./ (maximum - minimum);

end

function output_image = less_channels ( dwi, no_channels )

output_image = zeros(size(dwi.color_image));
for id_x = 1:size(dwi.color_image,1)
    for id_y = 1:size(dwi.color_image,2)
        if dwi.mask(id_x, id_y) == 1
            [val, index] = sort(dwi.color_image(id_x,id_y,:),'descend');
            output_image(id_x,id_y,index(1:no_channels)) = val(1:no_channels);
        end
    end
end

end
