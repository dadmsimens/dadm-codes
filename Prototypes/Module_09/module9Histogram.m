%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%        Function to create         %
%        image's histogram          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function [histIm] = module9Histogram(image)

image = image(:);         % vector of image

% ind=find(isnan(image)==1);
% image(ind)=0;
% ind=find(isinf(image)==1);
% image(ind)=0;
lengthImage = length(image);      % vector length
maxValue = ceil(max(image))+1;  % rounds each element of image to the nearest 
                                % integer greater than or equal to that element.
histIm = zeros(1,maxValue);  

for i = 1:lengthImage,            % create histogram of nanzero image value
    f = floor(image(i));          % round floor
    
    if (f>0 && f<(maxValue -1))        
        odds = image(i)-f;        % difference between image and round floor image value
        a1 = 1-odds;
        histIm(f) = histIm(f)  + a1;      
        histIm(f+1) = histIm(f+1)+ odds;                          
    end;
    
end;

histIm = conv(histIm,[1,2,3,2,1]);
histIm = histIm(3:(length(histIm)-2));
histIm = histIm/sum(histIm);