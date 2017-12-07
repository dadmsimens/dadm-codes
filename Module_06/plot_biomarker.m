function plot_biomarker( dwi, label )
%PLOT_BIOMARKER Summary of this function goes here
%   Detailed explanation goes here

figure;

switch(label)
    case 'all'
        subplot(2,2,1), plot_biomarker_single(dwi, 'MD');
        subplot(2,2,2), plot_biomarker_single(dwi, 'RA');
        subplot(2,2,3), plot_biomarker_single(dwi, 'FA');
        subplot(2,2,4), plot_biomarker_single(dwi, 'VR');        
    otherwise
        plot_biomarker_single(dwi, label)
end

end

function plot_biomarker_single( dwi, label )

switch(label)
    case 'MD'
        imshow(get_MD(dwi),[]);
        title('MD (Mean Diffusivity)');
    case 'RA'
        imshow(get_RA(dwi),[]);
        title('RA (Relative Anisotropy)');
    case 'FA'
        imshow(get_FA(dwi),[]);
        title('FA (Fractional Anisotropy)');
    case 'VR'
        imshow(get_VR(dwi),[]);
        title('VR (Volume Ratio)');
    otherwise
        error('Undefined biomarker label. Expected one of: MD, RA, FA, VR.');
end

end

