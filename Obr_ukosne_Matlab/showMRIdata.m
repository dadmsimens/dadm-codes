function showdata = showMRIdata(Imavol)

minI = min(min(min(Imavol)));       % min of all the data
maxI = max(max(max(Imavol)));       % max of all the data


for z=1:1:size(Imavol,3)
  I=(Imavol(:,:,z));
  I=I';
  scaledimg = (floor(((I - minI)./(maxI - minI))*255)); % perform scaling
 
    %convert the image to a true color image with the gray colormap.
  colorimg = ind2rgb(scaledimg,gray(256));
  g = hgtransform('Matrix',makehgtform('translate',[0 0 z]));
  imagesc(g,colorimg)
end
view(3)

axis([-20 1.2*size(Imavol,1) -20 1.2*size(Imavol,2) -20 1.2*size(Imavol,3)])
xlabel('x')
ylabel('y')
zlabel('z')

end