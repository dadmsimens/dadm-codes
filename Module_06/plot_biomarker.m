function plot_biomarker( eig_image, label )
%PLOT_BIOMARKER Summary of this function goes here
%   Detailed explanation goes here

figure;

switch(label)
    case 'all'
        subplot(2,2,1), plot_biomarker_single(eig_image, 'MD');
        subplot(2,2,2), plot_biomarker_single(eig_image, 'RA');
        subplot(2,2,3), plot_biomarker_single(eig_image, 'FA');
        subplot(2,2,4), plot_biomarker_single(eig_image, 'VR');        
    otherwise
        plot_biomarker_single(eig_image, label)
end

end

function plot_biomarker_single( eig_image, label )

switch(label)
    case 'MD'
        imshow(get_MD(eig_image),[]);
        title('MD (Mean Diffusivity)');
    case 'RA'
        imshow(get_RA(eig_image),[]);
        title('RA (Relative Anisotropy)');
    case 'FA'
        imshow(get_FA(eig_image),[]);
        title('FA (Fractional Anisotropy)');
    case 'VR'
        imshow(get_VR(eig_image),[]);
        title('VR (Volume Ratio)');
    otherwise
        error('Undefined biomarker label. Expected one of: MD, RA, FA, VR.');
end

end

