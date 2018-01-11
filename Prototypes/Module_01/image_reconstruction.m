% Function for reconstruction of subsampled MRI (aliased) images 
% using different methods 
% 
% INPUTS:
%   x_space_subsampled - subsampled data in x-space (size: FOX_y/subsamp_rate  x  FOX_x)
%   SensMaps - coil_sensitivities - maps of coils sensitivities (size: FOX_y  X  FOX_x  X  coils)
%   subsamp_rate - subsampling rate,
%   n_coils - numbers of receiver coils,
%   method - method chosen for reconstrucion 
%   lambda - regularization parameter (possible more than one value)
%            possible choices of methods:
%      method = 1 - SENSE reconstruction with LSE method
%      method = 2 - SENSE reconstruction with Tikhonov method
%      method = 3 - SENSE reconstruction with Tikhonov method 
%                   (with reference image)
%    lambda - regularization parameter (single value or vector of values),
%    ref_image - reference image (obtained using SoS (sum of squares method))
%
% OUTPUTS:
%   recon_image - reconstructed image using different methods

function recon_image = image_reconstruction(x_space_subsamp, SensMaps, r, nc, method, lambda, image, gradients)

[Mx, My, S, L] = size(x_space_subsamp);

ND=ndims(x_space_subsamp);

Ss = zeros(nc, 1);      % aliased data for certain point in reduced FOVy
% C = zeros(nc, r);       % coefficients of sensitivity maps for certain points in reduced FOVy                 
Sr = zeros(r, 1);       % reconstructed points in full FOVy 
FOVy = size(x_space_subsamp, 1);  % reduced FOVy size -> "moving" factor

% central line must be in the center while reconstructing:
% x_space = movedata(x_space_subsamp, subsamp_rate);
I = eye(r);
%%
% full FOV image reconstruction depending on the choice of the method 
for n=1:Mx
    for m=1:My
            
        if ND==4
            for s=1:S
            Cc=squeeze(SensMaps(n:Mx:(n+Mx*(r-1)),m,:));
            C=abs(transpose(Cc));
            Ss=squeeze(abs(x_space_subsamp(n,m,s,:)));
            
            if(method==1)
                Sr = transpose(inv(C'*C)*C'*Ss);
            elseif(method==2)
                Sr = transpose(inv(C'*C+lambda*I)*C'*Ss);
            elseif(method==3)
                ref_img = image(n:Mx:(n+Mx*(r-1)),m,s); 
                Sr = transpose(ref_img + inv(C'*C + lambda*I)*C'*(Ss - C*ref_img));
            elseif(method==4 || method==5)
                Ss_grad = zeros(size(gradients,1)*L,1);
                Ss_data = squeeze(abs(x_space_subsamp(n,m,2:S,:)));
                for ss=2:S
                    if ss >= 2
                       weights = zeros(1,S-1);
                       mainDirection = gradients(ss-1,:);
                       mainSs = squeeze(abs(x_space_subsamp(n,m,ss,:)));
                       Gi = gradients;
                       Gi(ss-1,:) = [];
                       for p=1:size(Gi,1)
                           v = Gi(p,:);
                           weights_dir(p) = acos(dot(mainDirection,v)./(norm(mainDirection)*norm(v)));
                       end
                       weights_norm = weights_dir./max(weights_dir);
                       mainWeight = sum(weights_norm);
                       weights = cat(2, mainWeight, weights_norm);
                    end
                end
                Ss_data((ss-1),:) = [];
                Ss_grad = cat(1,mainSs, reshape(Ss_data, [(S-2)*L,1]));  
                wGi = repmat(weights, [L,1]); wGi=wGi(:);
                Cc=squeeze(SensMaps(n:Mx:(n+Mx*(r-1)),m,:));
                C=abs(transpose(Cc));
                C_grad = repmat(C,[S-1,1]);
%                 if (method==4)     
                    Sr = transpose(inv(C_grad'*C_grad)*C_grad'*(wGi.*Ss_grad));
%                 elseif (method==5)
%                     ref_img = image(n:Mx:(n+Mx*(r-1)),m,s); 
%                     Sr = transpose(ref_img + inv(C_grad'*C_grad + lambda*I)*C_grad'*wGi.*(Ss_grad - C_grad*ref_img));
%                 end
                Sr
            end
            recon_img(n:Mx:(n+Mx*(r-1)),m,s) = Sr; 
            end
            
        elseif ND==3
            Cc=squeeze(SensMaps(n:Mx:(n+Mx*(r-1)),m,:));
            C=transpose(abs(Cc));
            Ss=squeeze(abs(x_space_subsamp(n,m,:)));

            if(method==1)
                Sr = transpose(inv(C'*C)*C'*Ss);
            elseif(method==2)
                Sr = transpose(inv(C'*C+lambda*I)*C'*Ss);
            elseif(method==3)
                ref_img = image(n:Mx:(n+Mx*(r-1)),m); 
                Sr = transpose(ref_img + inv(C'*C + lambda*I)*C'*(Ss - C*ref_img));
            end
            
            recon_img(n:Mx:(n+Mx*(r-1)),m) = Sr;
        end
    end
end
% points selected from each coil for reconstrucion
recon_image = abs(recon_img);
end
