close all;
clear all;
clc; 

fontSize = 11;

%% Load brain MRI data without skull

i = load('skullFreeImage.mat');
image = i.skullFreeImage;

[rows, columns, nrColorChannel] = size(image);

% Displey the image 
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

subplot(1,3,2:3);
histogr = histogram(image);
thresh = multithresh(image,3);                      % Histogram of non-zeros image
[pixelCounts, grayLevels] = imhist(uint8(image));
histo = histogram(image(image>=thresh(1)));

% Set histogram properties
lastGrayLevel = find(pixelCounts>0, 1, 'last');
xlim([0, lastGrayLevel]);                           % Set up axis range
grid on;
ax = gca;
ax.XTick = 0 : 50 : lastGrayLevel;                  % Set up tick marks every 50 gray levels.
title('Histogram of Non-Black Pixels', 'FontSize', fontSize, 'Interpreter', 'None');
xlabel('Gray Level', 'FontSize', fontSize);
ylabel('Pixel Counts', 'FontSize', fontSize);


% %% Segmentation by thresholds
% 
% imCerebrospinal = zeros(size(image));
% imGrayMatter = zeros(size(image));
% imWhiteMatter = zeros(size(image));
% 
% for i=1:rows
%     for j=1:columns
%         if image(i,j) > thresh(1) && image(i,j) < thresh(2)
%             imCerebrospinal(i,j) = 0.33;                     % P�yn m�zgowo-rdzeniowy
%         elseif image(i,j) > thresh(2) && image(i,j) < thresh(3)
%             imGrayMatter(i,j) = 0.66;                   % Istota szara
%         elseif image(i,j) > thresh(3)
%             imWhiteMatter(i,j) = 1;                     % Istota bia�a
%         end
%     end
% end
% 
% segmentedBain = imCerebrospinal + imGrayMatter + imWhiteMatter;
% 
% % Set color for segmented elements of brain
% 
% % colorBackground = uisetcolor([0 0 0], 'Background');                % t�o
% % colorWhiteMatter = uisetcolor([1 1 1], 'White Matter ');            % istota bia�a
% % colorGrayMatter = uisetcolor([0.8 0.8 0.8], 'Gray Matter');         % istota szara
% % colorCerebrum = uisetcolor([0.302 0.7451 0.9333], 'Cerebrum');      % p�yn m�zgowo-rdzeniowy
% 
% figure;
% subplot(1,3,1)
% imshow(imCerebrospinal,[]);
% subplot(1,3,2)
% imshow(imWhiteMatter,[]);
% subplot(1,3,3)
% imshow(imGrayMatter,[]);
% 
% %  Set up figure properties
% set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
% set(gcf, 'Toolbar', 'none', 'Menu', 'none');
% set(gcf, 'Name', 'Segmentation', 'NumberTitle', 'Off');
% 
% map_imBackground = [0 0 0];
% map_imCerebrospinal = [0.302 0.7451 0.9333];
% map_imWhiteMatter = [1 1 1];
% map_imGrayMatter = [0.8 0.8 0.8];
% 
% figure;
% imshow(segmentedBain,[]); hold on;
% map = [map_imBackground; map_imCerebrospinal; map_imGrayMatter; map_imWhiteMatter];
% colormap(map);
% 
% %% Saving segmented image 
% 
% save('Cerebrospinal.mat','imCerebrospinal');
% save('WhiteMatter.mat','imWhiteMatter');
% save('GrayMatter.mat','imGrayMatter');
% save('SegmentedBrain.mat','segmentedBain');
% 
% %% 
% % 
% % grayLevels
% % pixelCounts
% % thresh
% 
% image_data = zeros(size(histo.Data));
% j=1;
% 
% for i = 1:19936
%     
%    if thresh(1) == histo.Data(i)
%        ind(j) = i;
%        j = j+1;
%    end
%    
% end
% 
% 

%% STEP 1a: Generate data from two 1D distributions.


imhist(uint8(image));
thresh = multithresh(image,3);

figure;
[pixelCounts, grayLevels] = imhist(uint8(image));
hold on;
plot(grayLevels, pixelCounts, 'r');

ilosc_pixeli = rows*columns;
% x = zeros(ilosc_pixeli, 1);
% p = zeros(pixelCounts(1));
% X = p;
% 
% for i = 2:size(grayLevels);
%     p = zeros(pixelCounts(i)) + grayLevels(i);
%     X = [X p];
% end

%% 


% check image
ima=double(image);
copy=ima;           % make a copy
ima=ima(:);         % vectorize ima
mi=min(ima);        % deal with negative 
ima=ima-mi+1;       % and zero values
m=max(ima);
s=length(ima);

% create image histogram

h=histogram(ima);
x=find(h);
h=h(x);
x=x(:);h=h(:);

% initiate parameters
k = 4;
mu=(1:k)*m/(k+1);
v=ones(1,k)*m;
p=ones(1,k)*1/k;

% start process

sml = mean(diff(x))/1000;
while(1)
        % Expectation
        prb = distribution(mu,v,p,x);
        scal = sum(prb,2)+eps;
        loglik=sum(h.*log(scal));
        
        %Maximizarion
        for j=1:k
                pp=h.*prb(:,j)./scal;
                p(j) = sum(pp);
                mu(j) = sum(x.*pp)/p(j);
                vr = (x-mu(j));
                v(j)=sum(vr.*vr.*pp)/p(j)+sml;
        end
        p = p + 1e-3;
        p = p/sum(p);

        % Exit condition
        prb = distribution(mu,v,p,x);
        scal = sum(prb,2)+eps;
        nloglik=sum(h.*log(scal));                
        if((nloglik-loglik)<0.0001) break; end;        

        clf
        plot(x,h);
        hold on
        plot(x,prb,'g--')
        plot(x,sum(prb,2),'r')
        drawnow
end

% calculate mask
mu=mu+mi-1;   % recover real range
s=size(copy);
mask=zeros(s);

for i=1:s(1),
    for j=1:s(2),
         for n=1:k
             c(n)=distribution(mu(n),v(n),p(n),copy(i,j)); 
         end
       a=find(c==max(c));  
         mask(i,j)=a(1);
    end
end

% 
% h=conv(h,[1,2,3,2,1]);
% h=h(3:(length(h)-2));
% h=h/sum(h);















% 
% mu1 = thresh(1);
% sigma1 = 2;
% m1 = 85;
% 
% mu2 = thresh(2);
% sigma2 = 4;
% m2 = 85;
% 
% mu3 = thresh(3);
% sigma3 = 6;
% m3 = 86;
% 
% % Data
% 
% X2 = pixelCounts;
% X1 = grayLevels;
% 
% %% STEP 1b: Plot the data points and their pdfs.
% 
% x = 1:1:256;
% 
% y1 = gaussian1D(x, mu1, sigma1);
% y2 = gaussian1D(x, mu2, sigma2);
% 
% figure;
% hold off;
% plot(x, y1, 'b-');
% hold on;
% plot(x, y2, 'r-');
% plot(X1(1:85), zeros(size(X1(1:85))), 'bx', 'markersize', 10);
% plot(X1(86:170), zeros(size(X1(86:170))), 'rx', 'markersize', 10);
% plot(X1(171:256), zeros(size(X1(171:256))), 'gx', 'markersize', 10);
% 
% set(gcf,'color','white') % White background for the figure.
% 
% % %% STEP 2: Choose initial values for the parameters.
% % 
% % % Set 'm' to the number of data points.
% % m = size(X, 1);
% % 
% % % Set 'k' to the number of clusters to find.
% % k = 3;
% % 
% % % Randomly select k data points to serve as the means.
% % indeces = randperm(m);
% % mu = zeros(1, k);
% % for (i = 1 : k)
% %     mu(i) = X(indeces(i));
% % end
% % 
% % % Use the overal variance of the dataset as the initial variance for each cluster.
% % sigma = ones(1, k) * sqrt(var(X));
% % 
% % % Assign equal prior probabilities to each cluster.
% % phi = ones(1, k) * (1 / k);
% % 
% % %%===================================================
% % %% STEP 3: Run Expectation Maximization
% % 
% % % Matrix to hold the probability that each data point belongs to each cluster.
% % % One row per data point, one column per cluster.
% % W = zeros(m, k);
% % 
% % % Loop until convergence.
% % for (iter = 1:1000)
% %     
% %     fprintf('  EM Iteration %d\n', iter);
% % 
% %     %%===============================================
% %     %% STEP 3a: Expectation
% %     %
% %     % Calculate the probability for each data point for each distribution.
% %     
% %     % Matrix to hold the pdf value for each every data point for every cluster.
% %     % One row per data point, one column per cluster.
% %     pdf = zeros(m, k);
% %     
% %     % For each cluster...
% %     for (j = 1 : k)
% %         
% %         % Evaluate the Gaussian for all data points for cluster 'j'.
% %         pdf(:, j) = gaussian1D(X, mu(j), sigma(j));
% %     end
% %     
% %     % Multiply each pdf value by the prior probability for each cluster.
% %     %    pdf  [m  x  k]
% %     %    phi  [1  x  k]   
% %     %  pdf_w  [m  x  k]
% %     pdf_w = bsxfun(@times, pdf, phi);
% %     
% %     % Divide the weighted probabilities by the sum of weighted probabilities for each cluster.
% %     %   sum(pdf_w, 2) -- sum over the clusters.
% %     W = bsxfun(@rdivide, pdf_w, sum(pdf_w, 2));
% %     
% %     %%===============================================
% %     %% STEP 3b: Maximization
% %     %%
% %     %% Calculate the probability for each data point for each distribution.
% % 
% %     % Store the previous means so we can check for convergence.
% %     prevMu = mu;    
% %     
% %     % For each of the clusters...
% %     for (j = 1 : k)
% %     
% %         % Calculate the prior probability for cluster 'j'.
% %         phi(j) = mean(W(:, j));
% %         
% %         % Calculate the new mean for cluster 'j' by taking the weighted
% %         % average of *all* data points.
% %         mu(j) = weightedAverage(W(:, j), X);
% %     
% %         % Calculate the variance for cluster 'j' by taking the weighted
% %         % average of the squared differences from the mean for all data
% %         % points.
% %         variance = weightedAverage(W(:, j), (X - mu(j)).^2);
% %         
% %         % Calculate sigma by taking the square root of the variance.
% %         sigma(j) = sqrt(variance);
% %     end
% %     
% %     % Check for convergence.
% %     % Comparing floating point values for equality is generally a bad idea, but
% %     % it seems to be working fine.
% %     if (mu == prevMu)
% %         break
% %     end
% % 
% % % End of Expectation Maximization loop.    
% % end
% % 
% % %%=====================================================
% % %% STEP 4: Plot the data points and their estimated pdfs.
% % 
% % x = [0:0.1:30];
% % y1 = gaussian1D(x, mu(1), sigma(1));
% % y2 = gaussian1D(x, mu(2), sigma(2));
% % 
% % % Plot over the existing figure, using black lines for the estimated pdfs.
% % plot(x, y1, 'k-');
% % plot(x, y2, 'k-');

