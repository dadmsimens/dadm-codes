function [interp_image]=initial_interp(image, N, M, display)
%if display==1, function displays before and after image 
%lf - interpolation factor - interpolated signal is lf-times lonnger than
%input data, so N-horizontal extension, M-vertical extension

lf=[N, M];
s=size(image).*lf;
step=(1+lf)/2; %interpolation step

%interpolation-szukanie wartoœci pixela znajduj¹cego siê pomiêdzy pixelami
%o znanych wartoœciach
[x, y]=ndgrid(step(1):lf(1):1-step(1)+s(1), step(2):lf(2):1-step(2)+s(2));
[xi, yi]=ndgrid(1:s(1), 1:s(2));
interp_image=interpn(x, y, image, xi, yi, 'spline');

%extraploation-szukanie wartoœci pixela znajduj¹cego siê poza zakresem,
%prognozowanie jak funkcja zachowuje siê poza zakresem, tutaj brzegowe
%wartoœci
%floor - rounds DOWN to the nearest integer
for i=1:floor(N/2)
    interp_image(i,:)=interp_image(floor(N/2)+1,:); %1st row=2nd row
end

for i=1:floor(M/2)
    interp_image(:,i)=interp_image(:,floor(N/2)+1); %1st column=2nd column
end

for i=1:floor(N/2)
   interp_image(s(1)-i+1,:)=interp_image(s(1)-floor(N/2),:); %last row
end

for i=1:floor(M/2)
   interp_image(:,s(1)-i+1)=interp_image(:,s(1)-floor(M/2)); %last column
end

if display==1
    figure(1); imshow(image, [])
    figure(2); imshow(interp_image, [])
end
end

