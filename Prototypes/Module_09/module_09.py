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

image= array([[1.,3.,6.],[1.,2.,6.]])
imageHistogram = imHist(image)
print(imageHistogram)

""" Create Gauss mixture model function """
def gmm(x,mu,v,p):
    print(imageGmm)

""" Segmentation - main function """
def segmentation(skullFreeImage):
    print(imageSegmentation)
