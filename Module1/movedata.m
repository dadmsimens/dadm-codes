% Function
% INPUTS
% OUTPUTS
function x_space_subsamp_moved = movedata(x_space_subsampled, subsamp_rate)

[Mx, My, n_coils] = size(x_space_subsampled);
FOVy = Mx;
if mod(subsamp_rate,2)==0 % subsamp_rate is even number
    img  = x_space_subsampled;
	x_space_subsampled(1:(FOVy/2),:,:) = img((FOVy/2+1):FOVy,:,:);
	x_space_subsampled((FOVy/2+1):FOVy,:,:) = img(1:(FOVy/2),:,:);
end
x_space_subsamp_moved = x_space_subsampled;
end