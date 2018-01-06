load('test_data_jaLMMSE');
DWInoisy = double(DWInoisy);

%%
tic;
DWIfiltered = UNLMD(DWInoisy, Grads, sigma, 2, 1);


etime = toc;
disp(['UNLM and all gradients: ',num2str(etime),' seconds']);

slice = 33;
grad  = 3;

%present results in one diagram
subplot(1,2,1),imshow(DWInoisy(:,:,slice,grad),[]),title('noisy');
subplot(1,2,2),imshow(DWIfiltered(:,:,slice,grad),[]),title('UNLM');