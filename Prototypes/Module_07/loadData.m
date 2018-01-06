function [image,image2, image3] = loadData(filename)
load(filename);
imageArray = SENSE_Tikhonov;
imageArray2 = SENSE_Tikhonov_ref_01;
imageArray3 = SENSE_LSE;
image = mat2gray(imageArray);
image2 = mat2gray(imageArray2);
image3 = mat2gray(imageArray3);
end
