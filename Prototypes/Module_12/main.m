[Imavol,scaninfo]= loadminc('t1_icbm_normal_1mm_pn0_rf0.mnc');
tic
showMRIdata(Imavol);

[X,Y,Z] = TransRotatePlane(Imavol,100,45,45,0);

InterpolatedImage=interpolateMRI(Imavol,X,Y,Z);
figure
imshow(InterpolatedImage,[]);
toc