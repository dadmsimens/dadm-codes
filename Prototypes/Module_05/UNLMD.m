function output = UNLMD (image, grads, map, rsim, rsearch)

%get size for indexes
[Y,X,Z,N] = size(image);

%set space for filtered image
output = zeros(Y,X,Z,N);

%separate gradients from baselines
separate = sqrt(sum(grads.*grads,2));
temp_base = (separate <= 0.01);
temp_gradients = (separate > 0.01);
gradients = image(:, :, :, temp_gradients); %89

%gradients table normalization
grads(temp_gradients,1) = grads(temp_gradients,1)./separate(temp_gradients);
grads(temp_gradients,2) = grads(temp_gradients,2)./separate(temp_gradients);
grads(temp_gradients,3) = grads(temp_gradients,3)./separate(temp_gradients);
grads(temp_base,:) = 0;

%RGB
weight_R = abs(grads(temp_gradients,1));
weight_R = weight_R./sum(weight_R);
weight_G = abs(grads(temp_gradients,2));
weight_G = weight_G./sum(weight_G);
weight_B = abs(grads(temp_gradients,3));
weight_B = weight_B./sum(weight_B);

nwr = sum(weight_R.*weight_R);
nwg = sum(weight_G.*weight_G);
nwb = sum(weight_B.*weight_B);
nwrgb = nwr + nwg + nwb;

rc = zeros(Y,X,Z);
gc = zeros(Y,X,Z);
bc = zeros(Y,X,Z);

for idx = 1:length(weight_R)
    rc = rc + weight_R(idx).*gradients(:,:,:,idx);
    gc = gc + weight_G(idx).*gradients(:,:,:,idx);
    bc = bc + weight_B(idx).*gradients(:,:,:,idx);
end

%spatial mean values of each channel
[muR,GxR,GyR,GzR,factorsR,hcorrR] = local_feat(rc, rsearch);
hcorrR = hcorrR*1.5;
hcorrR = hcorrR*hcorrR;

[muG,GxG,GyG,GzG,factorsG,hcorrG] = local_feat(gc, rsearch);
hcorrG = hcorrG*1.5; 
hcorrG = hcorrG*hcorrG;

[muB,GxB,GyB,GzB,factorsB,hcorrB] = local_feat(bc, rsearch);
hcorrB = hcorrB*1.5;
hcorrB = hcorrB*hcorrB;

%local moments: 2nd and 4th
for y = 1:Y
    for x = 1:X
        for z = 1:Z
            %no mask so...
            %neighbourhoods
            my = max(y-rsim, 1);
            MY = min(y+rsim, Y);
            mx = max(x-rsim, 1);
            MX = min(x+rsim, X);
            mz = max(z-rsim, 1);
            MZ = min(z+rsim, Z);
            
            %center values
            mu0R = muR(y,x,z); mu0G = muG(y,x,z); mu0B = muB(y,x,z);
            gx0R = GxR(y,x,z); gx0G = GxG(y,x,z); gx0B = GxB(y,x,z);
            gy0R = GyR(y,x,z); gy0G = GyG(y,x,z); gy0B = GyB(y,x,z);
            gz0R = GzR(y,x,z); gz0G = GzG(y,x,z); gz0B = GzB(y,x,z);
            
            %mean values and grads in neighbourhood
            muiR = muR(my:MY,mx:MX,mz:MZ); muiG = muG(my:MY,mx:MX,mz:MZ); muiB = muB(my:MY,mx:MX,mz:MZ);
            gxiR = GxR(my:MY,mx:MX,mz:MZ); gxiG = GxG(my:MY,mx:MX,mz:MZ); gxiB = GxB(my:MY,mx:MX,mz:MZ);
            gyiR = GyR(my:MY,mx:MX,mz:MZ); gyiG = GyG(my:MY,mx:MX,mz:MZ); gyiB = GyB(my:MY,mx:MX,mz:MZ);
            gziR = GzR(my:MY,mx:MX,mz:MZ); gziG = GzG(my:MY,mx:MX,mz:MZ); gziB = GzB(my:MY,mx:MX,mz:MZ);
            
            %distances from center
            distsR = (muiR-mu0R).*(muiR-mu0R) + ...
                    (gxiR-gx0R).*(gxiR-gx0R)*factorsR(1) + ...
                    (gyiR-gy0R).*(gyiR-gy0R)*factorsR(2) + ...
                    (gziR-gz0R).*(gziR-gz0R)*factorsR(3);
            distsG = (muiG-mu0G).*(muiG-mu0G) + ...
                    (gxiG-gx0G).*(gxiG-gx0G)*factorsG(1) + ...
                    (gyiG-gy0G).*(gyiG-gy0G)*factorsG(2) + ...
                    (gziG-gz0G).*(gziG-gz0G)*factorsG(3);
            distsB = (muiB-mu0B).*(muiB-mu0B) + ...
                    (gxiB-gx0B).*(gxiB-gx0B)*factorsB(1) + ...
                    (gyiB-gy0B).*(gyiB-gy0B)*factorsB(2) + ...
                    (gziB-gz0B).*(gziB-gz0B)*factorsB(3);
                
            %distances normalized
            distances = ( distsR./hcorrR + distsG./hcorrG + distsB./hcorrB ) ./ (nwrgb*map*map);
            
            %weights
            weight = exp(-distances);
            %avoid overfitting to central -> create_penalty like
            weight(weight>0.367879441171442) = 0.367879441171442;
            %normalize weight
            sum_weight = sum(weight(:));
            weight = weight./sum_weight;
            
            %take a moment for moments
            vals  = image(my:MY,mx:MX,mz:MZ,:);
            vals2 = vals.*vals;
            %vals4 = vals2.*vals2;
            weight = repmat(weight, [1,1,1,N]);
            M2 = sum( sum( sum( vals2.*weight, 1), 2), 3);
            M2 = M2(:);
            %M4 = sum( sum( sum( vals4.*weight, 1), 2), 3);
            %M4 = M4(:);
            
            %noisy moments
            %vals  = image(y,x,z,:);
            %vals  = vals(:);
            %vals2 = vals.*vals;
            %difference  = vals2 - M2;
            M2 = max( M2-2*map*map, 1e-10 );
            %M4 = max( M4-8*sigma*sigma.*(M2+sigma*sigma), 1e-10 );
            
            output(y,x,z,:) = sqrt(M2);
        end
    end
end
return;
            
            
