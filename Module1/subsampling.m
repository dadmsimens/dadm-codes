% Function for subsampling data in k-space
%
% subsampling can be done only in phase encoding direction
% the size of subsampled image depends on the value of subsamp_rate(r): 
% phase_encoding(FOVy) x frequency_ encoding(FOVx) = (256/r) x 256
% subsampling scheme depends on chosen rate (r) 
% subsampling has to be done uniformly in phase-encoding direction
% INPUTS:
%        k-space data,
%        r - subsampling rate, can be even or odd number (anyways, central line
%            which is (FOV/2)+1 has to be subsampled)
%        n_coils - number of coils
% OUTPUTS:
%        k-space subsampled data

function [k_space_subsampled, locations] = subsampling(k_space_data, r, n_coils)

[Mx, My, C] = size(k_space_data);
if ((r==3) | (r==5))
    k_space_subsampled = zeros(floor(Mx/r)-1, My, C);
elseif ((r==2) | (r==4))
    k_space_subsampled = zeros(floor(Mx/r), My, C);
end

% subsampling scheme
locations_1 = (Mx/2+1-r):(-r):1;
locations_2 = (Mx/2+1):r:Mx;
subsamp_scheme = [flipud(locations_1(:)); locations_2(:)];

if(length(locations_1) > length(locations_2))
   subsamp_scheme = subsamp_scheme(2:length(subsamp_scheme));
elseif(length(locations_1) < length(locations_2))
   subsamp_scheme=subsamp_scheme(1:length(subsamp_scheme)-1);
end

for c=1:n_coils
    k_space_subsampled(:, :, c) = k_space_data(subsamp_scheme, :, c);
end
end
