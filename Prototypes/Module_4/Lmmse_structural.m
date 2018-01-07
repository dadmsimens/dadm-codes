function [Im_est]=Lmmse_structural(Im,Ws,sigma)

%calculate moments
sigma2 = sigma.^2;
Mn_4=filter2(ones(Ws),Im.^4)./prod(Ws);
Mn_2=filter2(ones(Ws),Im.^2)./(prod(Ws));
%estimate new image
K=1+(4.*sigma2.^2-4.*sigma2.*Mn_2)./(Mn_4-Mn_2.^2); %mij squ 
K=max(K,0);
Im_est=sqrt(Mn_2-2.*sigma2+K.*(Im.^2-Mn_2));
Im_est=abs(Im_est);