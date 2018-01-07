clear all
close all
%% load data
load test
%%
Ws=[7,7]
fim=Lmmse_structural(In,Ws,MapaR2);
%% visualization
diff = abs((fim - In));
figure
subplot(1,3,3);
imshow(fim,[])
title('after Lmmse')
subplot(1,3,1);
imshow(In,[]);
title('noisy')
subplot(1,3,2);
imshow(diff, [])
title('difference')
