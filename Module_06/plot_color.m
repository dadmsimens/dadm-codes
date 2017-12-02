function plot_color( color_image, type, figure_handle )
%PLOT_COLOR Summary of this function goes here
%   Detailed explanation goes here

% TODO: check if this is correct:
% red - x-axis
% green - y-axis
% blue - z-axis

if nargin < 3
    figure_handle = figure();
end

color_image = normalize_color(color_image);

switch(type)
    case 'one'
        color_image = less_channels(color_image, 1);
        imshow(color_image);
        title('Principal direction of diffusion - one channel');
    case 'two'
        color_image = less_channels(color_image, 2);
        imshow(color_image);
        title('Principal direction of diffusion - two channels');
    case 'three'
        imshow(color_image);
        title('Principal direction of diffusion - three channels');
    case 'all'
        subplot(1,3,1); plot_color(color_image, 'one', figure_handle);
        subplot(1,3,2); plot_color(color_image, 'two', figure_handle);
        subplot(1,3,3); plot_color(color_image, 'three', figure_handle);
end

end

function color_image = normalize_color ( color_image )

% normalize to 0-1 in each channel
minimum = repmat(min(min(min(color_image))),[size(color_image,1),size(color_image,2),3]);
maximum = repmat(max(max(max(color_image))),[size(color_image,1),size(color_image,2),3]);
color_image = (color_image - minimum) ./ (maximum - minimum);

end

function output_image = less_channels ( color_image, no_channels )

output_image = zeros(size(color_image));
for id_x = 1:size(color_image,1)
    for id_y = 1:size(color_image,2)
        [val, index] = sort(color_image(id_x,id_y,:),'descend');
        output_image(id_x,id_y,index(1:no_channels)) = val(1:no_channels);
    end
end

end
