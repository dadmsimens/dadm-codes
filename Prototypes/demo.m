colormap(gray)
%open the image
dataset_T1 = openBrainWebData('t1_icbm_normal_1mm_pn0_rf40.rawb', 181, 217, 181, 1);
slice = 70;
image = dataset_T1(:,:,slice);

%normalize data
image = image./max(image(:)).*255;

%add noise
sigma=10;
nimage=image+sigma*randn(size(image));

%denoise using NLM
fimage=NLM(image,5,2,sigma);

%otsu tresholding
level = graythresh(image); %this line does the Otsu thresholding method
%returns the threshold for separating background from foreground
oimage = fimage < level;
%oimage is the logical mask

%noise estimation from background
simage = nimage.^2; %squared magnitude of image
back = simage(oimage); %only background is taken to calculations
mean_back = mean(back);

%denoise using UNLM
sig = sqrt(mean_back/2);
sigma_kacper = 1.0352;
UNLM = sqrt(fimage.^2 - 2*sigma_kacper^2);
UNLM = abs(UNLM);

%%present results in one diagram
figure(1)
subplot(3,2,1),imagesc(image),title('oryginalne dane');
subplot(3,2,2),imagesc(nimage),title('zaszumione dane');
subplot(3,2,3),imagesc(fimage),title('filtr NLM');
subplot(3,2,4),imagesc(UNLM-nimage),title('reszty z odejmowania');
subplot(3,2,5),imagesc(oimage),title('maska do estymacji szumu');
subplot(3,2,6),imagesc(UNLM),title('filtr UNLM');


%{
figure(2)
colormap(gray), imagesc(image),title('oryginalne dane');
figure(3)
colormap(gray), imagesc(nimage),title('zaszumione dane');
figure(4)
colormap(gray), imagesc(fimage),title('filtr NLM');
figure(5)
colormap(gray), imagesc(UNLM-nimage),title('reszty z odejmowania');
figure(6)
colormap(gray), imagesc(oimage),title('maska do estymacji szumu');
figure(7)
colormap(gray), imagesc(UNLM),title('filtr UNLM');
%}



