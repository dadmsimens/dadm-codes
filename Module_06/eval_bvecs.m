function bvecs = eval_bvecs( bvecs, bvals )
%EVAL_BVECS Summary of this function goes here
%   Detailed explanation goes here

EPSILON = 1e-4;

for idx = 1:size(bvecs,1)
   if (norm(bvecs(idx,:)) > 1 + EPSILON) || (norm(bvecs(idx,:)) < 1 - EPSILON)
      warning('dwi.bvecs must be an array of unit-length vectors. Attemtping normalization...'); 
      if bvals(idx) ~= 0
        bvecs(idx,:) = bvecs(idx,:) / bvals(idx);
      else
          error('Vector normalization failed, corresponding dwi.bval is equal to 0.');
      end
   end
end

end

