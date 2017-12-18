function [X,Y,Z] = TransRotatePlane(Imavol,Trans,Rotx,Roty,Rotz)

v = [0,0,1];

Rx=rotx(Rotx);
Ry=roty(Roty);
Rz=rotz(Rotz);
v=v*Rx*Ry*Rz;

point=[size(Imavol,1)/2+Trans*abs(v(1))/(abs(v(1))+abs(v(2))+abs(v(3))),size(Imavol,2)/2+Trans*abs(v(2))/(abs(v(1))+abs(v(2))+abs(v(3))),1+Trans*abs(v(3))/(abs(v(1))+abs(v(2))+abs(v(3)))];
x1=point(1);
y1=point(2);
z1=point(3);

w = null(v); % Find two orthonormal vectors which are orthogonal to v
   [P,Q] = meshgrid(-1.2*max(size(Imavol)):1.2*max(size(Imavol))); % Provide a gridwork (you choose the size)
   X = x1+w(1,1)*P+w(1,2)*Q; % Compute the corresponding cartesian coordinates
   Y = y1+w(2,1)*P+w(2,2)*Q; %   using the two vectors in w
   Z = z1+w(3,1)*P+w(3,2)*Q;
   hold on
   surf(X,Y,Z,'edgecolor', 'yellow')

end
