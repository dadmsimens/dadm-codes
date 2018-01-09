clear all
close all
clc

m=matfile('recon_T1_synthetic_normal_1mm_L8_r2.mat');
image=m.SENSE_LSE;
tic
[upsampled, good, bad]=upsampling(image, 2, 2, 2, 1);
toc
[upsampled2, good2, bad2]=upsampling(upsampled, 1, 1, 2, 0);


% loop=0;
%bad-bad2=16396 -> 1 while loop execution
% while(1)
%     [upsampled2, good2, bad2]=upsampling(upsampled, 1, 1, 2, 0);
%     if bad-bad2<=16395
%         break;
%     end
%     loop=loop+1;
% end
figure(3); imagesc(upsampled2);colormap(gray); title('Upsampled image n-times');