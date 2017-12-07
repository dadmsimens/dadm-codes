function design_matrix = get_design_matrix( bvals, bvecs )
%GET_DESIGN_MATRIX Summary of this function goes here
%   Detailed explanation goes here

% TODO: derivation
design_matrix = -repmat(bvals,[1,6]) .* ...
    [bvecs(:,1).^2, bvecs(:,2).^2, bvecs(:,3).^2,...
    bvecs(:,1).*bvecs(:,2), bvecs(:,2).*bvecs(:,3), bvecs(:,1).*bvecs(:,3)];

end
