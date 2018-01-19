# coding: utf-8

import math, copy
import scipy.io as scio
import scipy as sc
import numpy as np
from scipy import *
from numpy import *

import simens_dadm as smns


""" Create histogrm function """

def imHist(image):
    image = image.flatten()

    lengthImage = image.size                # vector length
    maxValue = int(ceil(image.max())+1)     # rounds each element of image to the nearest
                                            # integer greater than or equal to that element.
    
    imageHistogram = np.zeros((1,maxValue))
    imageHistogram = imageHistogram.flatten()
    
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


""" Create Gauss mixture model function """

def gmm(x,mu,v,p):
        
    #x - column vector with non-zeros elemnts of histogram
    #mu - column vector expected value of each clasters
    #v - column vector of variation
    #p - column vector of probability
    
    x = (np.array(x)).flatten()
    mu = mu.flatten()
    v = v.flatten()
    p = p.flatten()
    
    probab = np.zeros([x.size, mu.size])   
    
    for i in range(mu.size):
        differ=x-mu[i]
        amplitude = p[i]/(math.sqrt(2*math.pi*v[i]))
        app = amplitude*(np.exp((-0.5*(differ*differ))/v[i]))
        probab[:,i] = app

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


def segmentation(skullFreeImage, pitches):
    
    [rows, columns, pitches]=skullFreeImage.shape
    print ("Pitche: " + str(pitches))
    print("size rows: " + str(rows) +  "    size columns: " + str(columns) + "    size pitches: " + str(pitches))
    pitches = pitches
    print ("pit: " + str(pitches))
    
    for pitch in range(0,pitches):
        
        print("pitch number: " + str(pitch))
        
        image = skullFreeImage[:,:,pitch]
        
        imageCopy = image
        im = image.flatten()
        imLength = im.size
        imMin = im.min()
        imMax = im.max()
        
        image = image-imMin + 1
        imageHistogram = imHist(image)
        x = np.nonzero(imageHistogram)
        hx = imageHistogram[x]

        clustersNum = 4
        mu = arange(1,clustersNum+1)*imMax/(clustersNum+1)
        v = np.ones(clustersNum)*imMax
        p = np.ones(clustersNum)/clustersNum
        
        condition = 1
        while condition == 1:
            
            #Expectation Step
            
            probab = gmm(x,mu,v,p)
            distrDens = probab.sum(axis=1)
            llh = (hx*np.log(distrDens)).sum()

            
            #Maximization Step
            
            for j in range(clustersNum):
                hxsh = hx.shape
                probabxh = probab.shape
                distsh=distrDens.shape
                resp = hx*probab[:,j]/distrDens
                p[j]=resp.sum()
                mu[j]=(x*resp/p[j]).sum()
                differ=x-mu[j]
                v[j]=(differ*differ*resp/p[j]).sum()
                
            p = p+0.001
            p = p/p.sum()
            
            
            #Exit alghoritm condition
            
            probab = gmm(x,mu,v,p)
            distrDens = probab.sum(axis=1)
            nllh = (hx*np.log(distrDens)).sum()
            diffLlh = nllh-llh
            
            if diffLlh<0.0001:
                condition = 0
            

        #Image mask
        
        mu = mu+imMin-1             #recover real range

        c = np.zeros(clustersNum)
        
        mri_segMask = np.zeros([rows, columns, pitches])
        print(mri_segMask.shape)
        
        for i in range(rows):
            for j in range(columns):
                for  k in range(clustersNum):
                    c[k] = gmm(image[i,j],mu[k],v[k],p[k])
                a = (c==c.max()).nonzero()
                
                mri_segMask[i,j,pitch]=a[0]            
    
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
        
#skullFreeImage = np.array([[[ 1,  1,  2],[ 3,  1,  2],[ 1, 1,  3]],[[ 2, 3, 1],[2, 1, 1],[1, 2, 2]],[[2, 3, 2],[1, 2, 3],[1, 2, 2]]])
#skullFreeImage = np.ndarray(shape=(3,2,2), dtype=float, order='F')+10
data = scio.loadmat('skullFreeImage_test.mat')
print(data)
skullFreeImage = data['imagesSkullFree']
#print("SkullFreeImage: " + str(skullFreeImage))
[rows, columns, pitches]=skullFreeImage.shape
#print(" size rows: " + str(rows) +  "size columns: " + str(columns) + "size pitches: " + str(pitches))
mri_segMask = segmentation(skullFreeImage,pitches)

scio.savemat('test.mat', {'mri_segMask':mri_segMask})

