function eval_bvecs( dwi )
%EVAL_dwi.bvecs Summary of this function goes here
%   Detailed explanation goes here

EPSILON = 1e-4;

for idx = 1:size(dwi.bvecs,1)
   if (norm(dwi.bvecs(idx,:)) > 1 + EPSILON) || (norm(dwi.bvecs(idx,:)) < 1 - EPSILON)
      warning('dwi.dwi.bvecs must be an array of unit-length vectors. Attemtping normalization...'); 
      if dwi.bvals(idx) ~= 0
        dwi.bvecs(idx,:) = dwi.bvecs(idx,:) / dwi.bvals(idx);
      else
          error('Vector normalization failed, corresponding dwi.bval is equal to 0.');
      end
   end
end

end

