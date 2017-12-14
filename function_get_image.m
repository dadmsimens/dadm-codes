function obl_image = function_get_image(slices_data,rotationx,rotationy,rotationz,translation)
len=length(slices_data);
plane=ones(1.5*len,1.5*len,2)*max(max(max(slices_data)));
% plane(:,:,1)=ones(256,256)*max(max(max(slices_data)));

rot_matrix=makehgtform('xrotate',rotationx,'yrotate',rotationy,'zrotate',rotationz);
% trans_matrix=makehgtform('translate',translation);

%  tform = affine3d(rot_matrix);
%  plane2=plane;
%  plane2=imwarp(plane2,tform);
%  len2=length(plane2);
% % 
% ind=(find(plane2(:,:,:)));
% ind=ind(1)
% [dimx,dimy,dimz]=size(plane2)
% % y=find(plane2(len2/2,:,z(1)))
% % x=find(plane2(len2/2,y(1),z(1)))
% % plane2(x(1),y(1),z(1))
% % save('plane2')
% [x,y,z]=ind2sub([dimx,dimy,dimz],ind)
% % trans_matrix=makehgtform('translate',translation);
% for i=1:dimx
%     for j=1:dimy
%         for k=1:dimz
%             plane3(i+x,j+y,z+k)=plane2(i,j,k);
%         end
%     end
% end
% 
% 
m = hgtransform('Matrix',rot_matrix);
% trans0=makeghtransform('translate',0);
% image(trans0,plane3)
%image(m,plane(:,:,1))
i=1;
for z=0:10:150
  img=slices_data(:,:,i);
  g = hgtransform('Matrix',makehgtform('translate',[0 0 z]));
  image(g,img)
  i=i+1;
end
view(3)

%imwarp(plane,tform);