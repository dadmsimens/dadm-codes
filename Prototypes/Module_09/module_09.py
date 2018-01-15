# coding: utf-8

import math, copy
import scipy.io as scio
import matplotlib.pyplot as plt
import scipy as sc
import numpy as np
from scipy import *
from numpy import *

import simens_dadm as smns

""" Create histogrm function """
"""
Matlab prototype:
function [histIm] = module9Histogram(image)

image = image(:);         % vector of image

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
"""

def imHist(image):
    image = image.flatten()

    lengthImage = image.size                # vector length
    maxValue = int(ceil(image.max())+1)     # rounds each element of image to the nearest
                                            # integer greater than or equal to that element.
    
    imageHistogram = zeros((1,maxValue))
    imageHistogram=imageHistogram.flatten()
    
    for i in range(lengthImage):
        f = int(floor(image[i]))
        if f>0:
            if f<maxValue:
                odds=image[i]-f             # difference between image and round floor image value
                a1=1-odds
                imageHistogram[f-1]=imageHistogram[f-1]+a1
                imageHistogram[f]=imageHistogram[f]+odds
    
    imageHistogram=np.convolve(imageHistogram,[1,2,3,2,1])
    imageHistogram=imageHistogram[2:(imageHistogram.size-2)]
    imageHistogram=imageHistogram/(imageHistogram.sum())
    return imageHistogram

#image= array([[1.,3.,6.],[1.,2.,6.]])
#imageHistogram = imHist(image)
#print(imageHistogram)

""" Create Gauss mixture model function """
"""
Matlab prototype
function y = module9GaussDist(x,mu,v,p)

% x - column vector with non-zeros elemnts of histogram
% mu - column vector expected value of each clasters
% v - column vector of variation
% p - column vector of probability

mu = mu(:);
v = v(:);
p = p(:);

for i=1:size(mu,1)
   differ = x-mu(i);
   amplitude = p(i)/sqrt(2*pi*v(i)); 
   y(:,i) = amplitude*exp(-0.5 * (differ.*differ)/v(i));
end

"""
def gmm(x,mu,v,p):
        
    #x - column vector with non-zeros elemnts of histogram
    #mu - column vector expected value of each clasters
    #v - column vector of variation
    #p - column vector of probability
    
    #x = x.flatten()
    mu = mu.flatten()
    v = v.flatten()
    p = p.flatten()
    
    probab = []
    
    for i in range(mu.size):
        differ=x-mu[i]
        amplitude = p[i]/(math.sqrt(2*math.pi*v[i]))
        app = amplitude*(np.exp((-0.5*(differ*differ))/v[i]))
        probab.extend(app)
    probab = np.array(probab)
    probab = np.transpose(probab)
    return(probab)
    
""" Segmentation - main function """
"""
Matlab prototype:
%% GMM for all images

imageAll = ima.imagesSkullFree;
% imageAll = ima;

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
        
        probab = module9GaussDist(x,mu,v,p);
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
                c(n) = module9GaussDist(imageCopy(i,j),mu(n),v(n),p(n)); 
            end
            
            a = find(c == max(c));  
            imageMask(i,j) = a(1);
        end
    end
    
    imageMaskFull(:,:,pitch) = imageMask;
%     pitch
end
"""


def segmentation(skullFreeImage,pitches):
    
    #pobranie wszystkich danych z modułu 8
    pitches = 3
    
    for pitch in range(pitches):
        
        image = skullFreeImage[pitch,:,:]
        print("I: " + str(image))
        
        imageCopy = image
        image = double(image)
        im = image.flatten()
        imLength = im.size
        imMin = im.min()
        imMax = im.max()
        
        image = image-imMin + 1
        print ("image: " + str(image))
        
        imageHistogram = imHist(image)
        print("imageHistigram: " + str(imageHistogram))
        x = imageHistogram.nonzero()
        print("x: " + str(x))
        hx = imageHistogram[x]
        print("hx: " + str(hx))
        
        clustersNum = 2
        mu = arange(1,clustersNum+1)*imMax/(clustersNum+1)
        v = np.ones(clustersNum)*imMax
        p = np.ones(clustersNum)/clustersNum
        print("mu: " + str(mu) + " v: " + str(v) + " p: " + str(p))
        
        condition = 1
        while condition == 1:
            
            #Expectation Step
            probab = gmm(x,mu,v,p)
            #probab = np.array(probab)
            #probab = array([[1,2,3],[1,1,1],[4,5,6]])
            print("probab trans: " + str(probab))
            distrDens = probab.sum(axis=1)
            print("distr Dens: " + str(distrDens))
            llh = (hx*np.log(distrDens)).sum()
            print("llh: " + str(llh))
            
            #Maximization Step
            for j in range(clustersNum):
                print(j)
                hxsh = hx.shape
                probabxh = probab.shape
                distsh=distrDens.shape
                print(" hx  " + str(hxsh) + " probab  " + str(probabxh) + " dist  " + str(distsh))
                resp = hx*probab[:,j]/distrDens
                print("resp: " + str(resp))
                p[j]=resp.sum()
                print("p(j): " + str(p))
                mu[j]=(x*resp/p[j]).sum()
                print("mu(j): " + str(mu))
                differ=x-mu[j]
                print("differ: " + str(differ))
                v[j]=(differ*differ*resp/p[j]).sum()
                print("v: " + str(v))
                
            print("P1: " + str(p[:]))
            p = p+0.001
            print("P2: " + str(p))
            p = p/p.sum()
            print("P3: " + str(p))
            
            #Exit alghoritm condition
            """ Błąd w warunku wyjściowym """
            probab = gmm(x,mu,v,p)
            distrDens = probab.sum(axis=1)
            nllh = (hx*np.log(distrDens)).sum()
            diffLlh = nllh-llh
            print("llh: " + str(llh))
            print("nlhh: " + str(nllh))
            print("diffLlh: " + str(diffLlh))
            
            #condition = 0
            if diffLlh<0.0001:
                break
            
        print("pitch number: " + str(pitch))
        #Image mask
        mu = mu+imMin-1             #recover real range
        imageMask = np.zeros([rows, columns])
        print("imageMask: " + str(imageMask))
        
        c = np.zeros(clustersNum)
        print("c: " + str(c))
        
        for i in range(rows):
            for j in range(columns):
                for  k in range(clustersNum):
                    c[k] = gmm(image[i,j],mu[k],v[k],p[k])
                a = (c==c.max()).nonzero()
                mri_segMask[i,j]=a[1]
                
        print("c: " + str(c))
        
        return mri_segMask
        
"""
    
    % Image mask 
    mu = mu+minImage-1;                                       % recover real range
    imageMask = zeros([rows columns]);

    for i = 1:rows
        for j = 1:columns
            for n = 1:clastersNum
                c(n) = module9GaussDist(imageCopy(i,j),mu(n),v(n),p(n)); 
            end
            
            a = find(c == max(c));  
            imageMask(i,j) = a(1);
        end
    end
    
    imageMaskFull(:,:,pitch) = imageMask;
%     pitch
end
"""
        
skullFreeImage = array([[[ 1,  1,  2],[ 3,  1,  2],[ 1, 1,  3]],[[ 2, 3, 1],[2, 1, 1],[1, 2, 2]],[[2, 3, 2],[1, 2, 3],[1, 2, 2]]])
print("SkullFreeImage: " + str(skullFreeImage))

[pitches, rows, columns]=skullFreeImage.shape
print("size pitches: " + str(pitches) + " size rows: " + str(rows) + " size columns: " + str(columns))
segmentation(skullFreeImage,pitches)
