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
%         possible choices of methods:
%      method = 1 - SENSE basic reconstruction
%      method = 2 - SENSE basic reconstruction with covariance matrix between coils
%      method = 3 - SENSE reconstruction with LSE method
%      method = 4 - SENSE reconstruction with Tikhonov method
%      method = 5 - SENSE reconstruction with Tikhonov method 
%                   (with reference image)
%    cbc - correlation between coils,
%    std - standard deviation, 
%    lambda - regularization parameter (single value or vector of values),
%    ref_image - reference image (obtained using SoS (sum of squares method))
%
% OUTPUTS:
%   recon_image - reconstructed image using different methods


function recon_image = image_reconstruction(k_space_subsamp, SensMaps, r, nc, method, rho, std, lambda, image, grad_maps)

% data
[Mx, My, nc] = size(SensMaps);
%recon_img = zeros(Mx,My);

% covariance matrix 
cov_mat = std.^2.*(eye(nc) + rho.*(ones(nc) - eye(nc))); 

% sigma matrix 
sigma_mat = std.^2.*(eye(nc));

if ((r==3) | (r==5))
    x_space= zeros(floor(Mx/r)-1, My, nc);
    red_Mx = floor(Mx/r)-1;
elseif ((r==2) | (r==4))
    x_space = zeros(floor(Mx/r), My, nc);
    red_Mx = floor(Mx/r);
end

x_space = k_to_x(k_space_subsamp, nc);

% Ss = C*Sr  - linear system of equatations
Ss = zeros(nc, 1);      % aliased data for certain point in reduced FOVy
C = zeros(nc, r);       % coefficients of sensitivity maps for certain points in reduced FOVy                 
Sr = zeros(r, 1);       % reconstructed points in full FOVy 
FOVy = size(x_space, 1);  % reduced FOVy size -> "moving" factor

% central line must be in the center while reconstructing, so if r is odd number,
% the overlapped image matrix will stay unchanged, otherwise:
% x_space = movedata(x_space_subsamp, subsamp_rate);
I = eye(r);

% full FOV image reconstruction depending on the choice of the method 
for n=1:red_Mx
    for m=1:My
  
            Cc=squeeze(SensMaps(n:red_Mx:(n+red_Mx*(r-1)),m,:));
            C=transpose(Cc);
            Ss=squeeze(abs(x_space(n,m,:)));
            
            if(method==1)
                %Sr = transpose(inv(C'*inv(sigma_mat)*C)*C'*inv(sigma_mat)*Ss);
                Sr = transpose(((C'*(sigma_mat\C))\C')*(sigma_mat\Ss));                
            elseif(method==2)
                Sr = transpose(inv(C'*inv(1./cov_mat)*C)*C'*inv(1./cov_mat)*Ss);
%             elseif(method==22)
%                 Sr = transpose(inv(C'*inv(1./cov_mat.^2)*C)*C'*inv(1./cov_mat.^2)*Ss);                                
%             elseif(method==222)
%                 Sr = transpose(inv(C'*inv(1./inv(cov_mat))*C)*C'*inv(1./inv(cov_mat))*Ss);                                                
            elseif(method==3)
                Sr = transpose(inv(C'*C)*C'*Ss);
            elseif(method==4)
                Sr = transpose(inv(C'*C+lambda*I)*C'*Ss);
            elseif(method==5)
                ref_img = image(n:red_Mx:(n+red_Mx*(r-1)),m); 
                Sr = transpose(ref_img + inv(C'*C + lambda*I)*C'*(Ss - C*ref_img));
            end
            
            recon_img(n:red_Mx:(n+red_Mx*(r-1)),m) = Sr;
            
            %gmaps
            pseudo_inv_matrix = pinv(C'*C).*(C'*C); 
            pseudo_inv_matrix = sqrt(abs(diag(pseudo_inv_matrix)));  
            gmap(n:red_Mx:(n+red_Mx*(r-1)),m)= pseudo_inv_matrix';
    end
end


% points selected from each coil for reconstrucion

recon_image = abs(recon_img);