function [filtered_image, good, bad]=upsampling(image, N, M, window, display)
%Initial B-spline interpolation
% N and M - extensions
image2=initial_interp(image, N, M, 0);
s=size(image2);
sigma=std2(image2);

level=sigma/2; %degree of filering
[X, Y]=meshgrid(-window:window, -window:window); 
tol=0.002*std2(image);

%%%%
% while(1)
% Reconstruction
filtered_image=zeros(s);
for i=2:s(1,1)
    for j=2:s(1,2)
         iMin = max(i-window,1); %creation of a window
         iMax = min(i+window,s(1,1));
         jMin = max(j-window,1);
         jMax = min(j+window,s(1,2));
         image_window = image2(iMin:iMax,jMin:jMax);

         %Intensity difference
         w1 = exp(-(abs(image_window-image2(i,j))).^2/(level^2)); %wy - okno o wymiarze image_window; ka¿da wartoœæ image_widnow pomniejszona o wartoœæ pixela image(i, j) 
         
         %Distance difference
         for k=iMin:iMax
             for m=jMin:jMax
                   w2=exp((-Euclidean_dist(k, m, i, j))/level^2);
             end
         end
         
         weight=w1.*w2;
         filtered_image(i,j)=sum(weight(:).*image_window(:))/sum(weight(:));
         
    end
end
%%%%
good=0; bad=0;
%Checking with tolerance - I have to do it better
for i=2:1:s(1,1)
    for j=2:1:s(1,2)
       if (abs(filtered_image(i, j)-filtered_image(i-1, j-1)) < tol) 
          good=good+1;
       else
           bad=bad+1;
       end
    end
end
% end

%Mean correction - equation 7
for i=1:N:s(1,1)
   for j=1:M:s(1,2)
      tmp=filtered_image(i:i+N-1, j:j+M-1);
      offset=image((i+N-1)/N, (j+M-1)/M)-mean(tmp(:)); %NN(D(x)-y) eq7
      image3(i:i+N-1, j:j+M-1)=filtered_image(i:i+N-1, j:j+M-1)+offset;      
   end
end

if display==1
    figure(1); imagesc(image);colormap(gray); title('Original image');
    figure(2); imagesc(filtered_image);colormap(gray); title('Upsampled image');
end
end
