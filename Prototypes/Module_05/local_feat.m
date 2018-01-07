function [mu, Gx, Gy, Gz, factors, hcorr] = local_feat(image, rsearch)

image = double(image);

%create gaussian windows for each dimension
gx = gausswin(2*rsearch + 1);
gx = gx./sum(gx);
gy = gausswin(2*rsearch + 1);
gy = gy./sum(gy);
gz = gausswin(2*rsearch + 1);
gz = gz./sum(gz);

%local mean
mu = My3DConv(image, gx, gy, gz);

%kernels for diff
gdx = (-rsearch:rsearch)';
gdx = (gdx.*gx)./sum(gdx.*gdx.*gx);
gdy = (-rsearch:rsearch)';
gdy = (gdy.*gy)./sum(gdy.*gdy.*gy);
gdz = (-rsearch:rsearch)';
gdz = (gdz.*gz)./sum(gdz.*gdz.*gz);

%create each gradient image (the minus sign is for consistence with the
%implementation of matlab's 'gradient' function)
Gx  = -My3DConv( image, gdx, gy,  gz  );
Gy  = -My3DConv( image, gx,  gdy, gz  );
Gz  = -My3DConv( image, gx,  gy,  gdz );

%compute the scaling factors:
factors(1) = sum( (-rsearch:rsearch).*(-rsearch:rsearch).*gx' );
factors(2) = sum( (-rsearch:rsearch).*(-rsearch:rsearch).*gy' );
factors(3) = sum( (-rsearch:rsearch).*(-rsearch:rsearch).*gz' );

%compute the correction in the h factor and x matrix
[x,y,z] = meshgrid( -rsearch:rsearch, -rsearch:rsearch, -rsearch:rsearch);
X = [ones(size(x(:))), ...
    x(:), y(:), z(:), ...
    x(:).*x(:)/2, y(:).*y(:)/2, z(:).*z(:)/2, ...
    x(:).*y(:), x(:).*z(:), y(:).*z(:) ];

[g1,g2,g3] = meshgrid(gx,gy,gz);
R = g1(:).*g2(:).*g3(:);
hcorr = sqrt(trace(diag(R)*X*(X'*X)^(-1)*X'));


return;

