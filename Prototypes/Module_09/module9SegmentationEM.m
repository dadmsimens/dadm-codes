close all; clear; clc;

fontSize = 12;

%% Load brain MRI data without skull

% i = load('skullFreeImage.mat');
% image = i.skullFreeImage;
% 
% [rows, columns, nrColorChannel] = size(image);

ima = load('skullFreeImage_test.mat');
[rows, columns, pitches, nrColorChannel] = size(ima.imagesSkullFree);
image = ima.imagesSkullFree(:,:,10);

%% Displey the image 

figure;
subplot (1,3,1);
imshow(image,[]);
axis on;
caption = sprintf('Non-skull brain MRI Image');
title(caption, 'FontSize', fontSize, 'Interpreter', 'None');

% Set up figure properties
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
set(gcf, 'Toolbar', 'none', 'Menu', 'none');
set(gcf, 'Name', 'Non-skull brain MRI image', 'NumberTitle', 'Off')

[rows, columns, nrColorChannel] = size(image);

%% Histogram of image and threshold selecting 

imageCopy = image;
subplot(1,3,2:3);
% histo = histogram(image);
thresh = multithresh(image,3);                      % Histogram of non-zeros image
[pixelCounts, grayLevels] = imhist(uint8(image));
imhist(uint8(image));
histo = histogram(image(image>=thresh(1)));

% Set histogram properties
lastGrayLevel = find(pixelCounts>0, 1, 'last');
xlim([0, lastGrayLevel]);                           % Set up axis range
ylim([0,750]);
grid on;
ax = gca;
ax.XTick = 0 : 20 : lastGrayLevel;                  % Set up tick marks every 50 gray levels.
title('Histogram of Non-Black Pixels', 'FontSize', fontSize, 'Interpreter', 'None');
xlabel('Gray Level', 'FontSize', fontSize);
ylabel('Pixel Counts', 'FontSize', fontSize);

%% Check image values

imageCopy = image;
image = double(image);
im = image(:);
lenghIm = length(im);                               % Image value in vector
minImage = min(im);
maxImage = max(im);
image = image - minImage + 1;                       % Deal with neagtive image value if exist

%% Image histogram

[histIm] = module9Histogram(image);
x = find(histIm)';                                  % Column with non-zeros elemnts
hx = histIm(x)';      

%% Parameter initialization

clastersNum = 4;                                    % Number of clusters
mu = (1:clastersNum)*maxImage/(clastersNum+1);      % Expected value of each clasters
v = ones(1,clastersNum)*maxImage;                   % Variation of each clasters (max image valu)
p = ones(1,clastersNum)*1/clastersNum;              % Probability of each clasters (0.25)


figure;                                             % Parameters visualisation
plot(histIm); hold on;
plot(mu, histIm(floor(mu)), 'r*');
plot(v, [0 0 0 0], 'b*');

%% Start alghoritm

while(1)
        
        % Expectation Step  
        probab = module9GaussDist(x,mu,v,p);           % Probability of belonging to a cluster
        distrDens = sum(probab,2);                     % The relativ densites 
        llh=sum(hx.*log(distrDens));                   % The log-likelihood base on histogram data
        
        
        %Maximization Step
        for j=1:clastersNum
                resp = hx.*probab(:,j)./distrDens;      % Compute the responsibilities
                p(j) = sum(resp);                       
                mu(j) = sum(x.*resp)/p(j);              % Compute the weighted means
                differ = (x-mu(j)); 
                v(j)=sum(differ.*differ.*resp)/p(j);% Computed the weighted variances
        end
        p = p + 1e-3;
        p = p/sum(p);                                   % Maxing probability

        
        % Exit alghoritm condition
        
        probab = distribution(mu,v,p,x);
        distrDens = sum(probab,2);
        nllh=sum(hx.*log(distrDens));                
        if((nllh-llh)<0.0001) 
            break; 
        end;        

        clf;
        plot(x,hx);
        hold on
        plot(x,probab,'g--')
        plot(x,sum(probab,2),'r')
        drawnow
end

% Image mask 
mu = mu+minImage-1;                                       % recover real range
imageMask = zeros([rows columns]);

for i = 1:rows
    for j = 1:columns
         for n = 1:clastersNum
             c(n) = distribution(mu(n),v(n),p(n),imageCopy(i,j)); 
         end
       a = find(c == max(c));  
       imageMask(i,j) = a(1);
    end
end

% Segmentation image
figure;
imshow(imageMask,[]);






%% GMM for all images

imageAll = ima.imagesSkullFree;

for pitch = 1:pitches
      
	image = imageAll(:,:,pitch);
    
    imageCopy = image;
    image = double(image);
    im = image(:);
    lenghIm = length(im);                               
    minImage = min(im);
    maxImage = max(im);
    image = image - minImage + 1; 
    
    [histIm] = module9Histogram(image);
    x = find(histIm)';
    hx = histIm(x)';      

    clastersNum = 4; 
    mu = (1:clastersNum)*maxImage/(clastersNum+1); 
    v = ones(1,clastersNum)*maxImage; 
    p = ones(1,clastersNum)*1/clastersNum;
    
    while(1)
        
        % Expectation Step  
        probab = module9GaussDist(x,mu,v,p); 
        distrDens = sum(probab,2);
        llh=sum(hx.*log(distrDens));
        
        %Maximization Step
        for j=1:clastersNum
                resp = hx.*probab(:,j)./distrDens;   
                p(j) = sum(resp);                       
                mu(j) = sum(x.*resp)/p(j);          
                differ = (x-mu(j)); 
                v(j)=sum(differ.*differ.*resp)/p(j);
        end
        p = p + 1e-3;
        p = p/sum(p);                                   
        
        % Exit alghoritm condition
        
        probab = distribution(mu,v,p,x);
        distrDens = sum(probab,2);
        nllh=sum(hx.*log(distrDens));                
        if((nllh-llh)<0.0001) 
            break; 
        end;        
    end

    % Image mask 
    mu = mu+minImage-1;                                       % recover real range
    imageMask = zeros([rows columns]);

	for i = 1:rows
        for j = 1:columns
            for n = 1:clastersNum
            	c(n) = distribution(mu(n),v(n),p(n),imageCopy(i,j)); 
            end
            
            a = find(c == max(c));  
            imageMask(i,j) = a(1);
        end
    end
    
    imageMaskFull(:,:,pitch) = imageMask;
%     pitch
end


%% Segmented parts exaple

% Gray Matter
gM = imageMaskFull(:,:,5)==3;
figure;
imshow(gM,[]);

% White Matter
wM = imageMaskFull(:,:,5)==4;
figure;
imshow(wM,[]);

% Cerebro-spinal fluid
csF = imageMaskFull(:,:,5)==2;
figure;
imshow(csF,[]);

%% Save segmentation mask

% save('segmentationMask.mat','imageMaskFull');