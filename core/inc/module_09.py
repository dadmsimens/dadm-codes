# coding: utf-8

import math, copy
import scipy.io as sio
import scipy as sc
import numpy as np
from scipy import *
from numpy import *

import simens_dadm as smns


""" Create histogrm function """

<<<<<<< HEAD

=======
>>>>>>> 6f6576e55c3d70d04896d30483db57c08082ac21
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


<<<<<<< HEAD
""" Create Gauss mixture model function """


=======


""" Create Gauss mixture model function """

>>>>>>> 6f6576e55c3d70d04896d30483db57c08082ac21
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


<<<<<<< HEAD
""" Segmentation - main function """


def segmentation(skullFreeImage):

    [rows, columns, pitches]=skullFreeImage.shape
    print ("Pitche: " + str(pitches))
    print("size rows: " + str(rows) +  "    size columns: " + str(columns) + "    size pitches: " + str(pitches))
    pitches = pitches
    print ("pit: " + str(pitches))
    


    for pitch in range(0,pitches-37):

        print("pitch number: " + str(pitch))
        im_test = skullFreeImage[:,:,pitch]
        #scio.savemat('test'+str(pitch)+'.mat', {'im_test':im_test})

        image = skullFreeImage[:,:,pitch]
=======


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

    mri_segMask = np.zeros([rows,columns, pitches])

    for pitch in range (pitches):

        print("Pitch:   " + str(pitch))

        image = imageToSeg[:,:,pitch]
>>>>>>> 6f6576e55c3d70d04896d30483db57c08082ac21

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

<<<<<<< HEAD

=======
>>>>>>> 6f6576e55c3d70d04896d30483db57c08082ac21
        #Image mask

        mu = mu+imMin-1             #recover real range
        c = np.zeros(clustersNum)
<<<<<<< HEAD
        imageMask = np.zeros([rows, columns])
=======

        imageMask = np.zeros([rows, columns])
       #print (imageMask.shape)


        #print("mri_segMask: " + str(mri_segMask))
>>>>>>> 6f6576e55c3d70d04896d30483db57c08082ac21

        for i in range(rows):
            for j in range(columns):
                for k in range(clustersNum):
                    c[k] = gmm(image[i,j],mu[k],v[k],p[k])
                a = (c==c.max()).nonzero()
                imageMask[i,j]=a[0]
<<<<<<< HEAD
        
        mri_segMask=imageMask
     
    return mri_segMask



""" Main body """


"""
def main9(mri_input, other_arguments = None):
	
    if (isinstance(mri_input, smns.mri_diff)): # instructions for diffusion mri

    # isinstance(mri_input, smns.mri_struct) returns TRUE for diffusion AND structural MRI because of inheritance.
    # It should be used if you have some code to work with BOTH structural and diffusion data (which may be frequent).

        mri_output = mri_input
        print("This file contains diffusion MRI")
        #some_code

    elif (isinstance(mri_input, smns.mri_struct)): # instructions specific for structural mri. The case of diffusion MRI is excluded here by elif.
        mri_data = mri_input
        print("This file contains structural MRI")
        #Segmentation
        mri_output = segmentation(mri_data)
    else:
        return "Unexpected data format in module number 9!"

    return mri_output """


data = sio.loadmat('skullFreeImage_test.mat')
skullFreeImage = data['imagesSkullFree']
mri_segMask = segmentation(skullFreeImage)


sio.savemat('test.mat', {'mri_segMask':mri_segMask})
	

=======

        #sio.savemat('test1.mat', {'test1':imageMask})
        print("imageMask shape: " + str(imageMask.shape))
        mri_segMask[:,:,pitch] = imageMask[:]

    return mri_segMask




""" Main body """

def main9(mri_input, other_arguments = None):

    if (isinstance(mri_input, smns.mri_struct)):
        [m,n,slices] = mri_input.structural_data.shape

        segmentationMask = segmentation(mri_input.structural_data)
        [rows, columns, sliceSeg] = segmentationMask.shape

        mri_output = np.zeros([m,n,sliceSeg])
        mri_output = segmentationMask

        mri_input.structural_data = mri_output

    else:
        return "Unexpected data format in module number 9!"

    return mri_input
>>>>>>> 6f6576e55c3d70d04896d30483db57c08082ac21
