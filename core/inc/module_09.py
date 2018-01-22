# coding: utf-8

import math, copy
import scipy.io as sio
import scipy as sc
import numpy as np
from scipy import *
from numpy import *



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




""" Part of image to segmentation """

def imPart(skullFreeImage, firstPitch, lastPitch, rows, columns, pitches):

    rangePitch = lastPitch - firstPitch
    imageToSeg = np.zeros([rows, columns, rangePitch])

    rPit = 0

    for pitch in range (pitches):
        if pitch < firstPitch:
            continue
        if pitch >= firstPitch:

            if pitch < lastPitch:
                imageToSeg [:,:,rPit] = skullFreeImage [:,:,pitch]
                rPit = rPit+1
            else:
                break

    return imageToSeg




""" Segmentation """

def segmentation(skullFreeImage):

    [rows, columns, pitches]=skullFreeImage.shape
    firstPitch = 70
    lastPitch = 140
    imageToSeg = imPart(skullFreeImage, firstPitch, lastPitch, rows, columns, pitches)

    pitches = lastPitch - firstPitch

    segmentImageMask = np.zeros([rows,columns, pitches])

    for pitch in range (pitches):

        print("Pitch:   " + str(pitch))

        image = imageToSeg[:,:,pitch]

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

        imageMask = np.zeros([rows, columns])

        for i in range(rows):
            for j in range(columns):
                for k in range(clustersNum):
                    c[k] = gmm(image[i,j],mu[k],v[k],p[k])
                a = (c==c.max()).nonzero()
                imageMask[i,j]=a[0]

        segmentImageMask[:,:,pitch] = imageMask[:]

    return segmentImageMask




""" Main body """

from . import simens_dadm as smns

def main9(mri_input, other_arguments = None):
    
    if isinstance(mri_input, smns.mri_struct):
        
        [m,n,slices] = mri_input.structural_data.shape
        
        segmentationMask = segmentation(mri_input.structural_data)
        [rows, columns, sliceSeg] = segmentationMask.shape
        
        mri_output.segmentation = np.zeros([m,n,sliceSeg])
        
        mri_output.segmentation = segmentationMask
        mri_input.structural_data = mri_output
        
    else:
        return "Unexpected data format in module number 9!"

    return mri_input


