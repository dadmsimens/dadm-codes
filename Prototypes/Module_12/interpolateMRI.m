function InterpolatedImage = interpolateMRI(Imavol,X,Y,Z)

xindmax = size(Imavol,1);
yindmax = size(Imavol,2);
zindmax = size(Imavol,3); 

xindmin=1;
yindmin=1;
zindmin=1;

pointsimage=[];

for i=1:size(X,1)
    for j=1:size(X,2)
        x0=round(X(i,j),1);
        y0=round(Y(i,j),1);
        z0=round(Z(i,j),1);
        
        if x0>xindmin && x0<=xindmax && y0>=yindmin && y0<=yindmax && z0>=zindmin && z0<=zindmax
        
        x01=floor(x0);
        x02=ceil(x0);
        y01=floor(y0);
        y02=ceil(y0);
        z01=floor(z0);
        z02=ceil(z0);
        
        if mod(x0,1) == 0 && mod(y0,1) == 0 && mod(z0,1) == 0
           pointsimage(i,j)=Imavol(x0,y0,z0);
        else
            
           if mod(x0,1) == 0 && mod(z0,1) == 0
                pointsimage(i,j)=(Imavol(x0,y01,z0)+Imavol(x0,y02,z0))/2;
           
           elseif mod(x0,1) == 0 && mod(y0,1)==0
                pointsimage(i,j)=(Imavol(x0,y0,z01)+Imavol(x0,y0,z02))/2;
           
           elseif mod(y0,1) == 0 && mod(z0,1) == 0
               pointsimage(i,j)=(Imavol(x01,y0,z0)+Imavol(x02,y0,z0))/2;
           else
               pointsimage(i,j)=Imavol(x01,y01,z01)+Imavol(x02,y01,z01)+Imavol(x01,y02,z01)+Imavol(x01,y01,z02)+Imavol(x01,y02,z02)+Imavol(x02,y01,z02)+Imavol(x02,y02,z02)+Imavol(x02,y02,z01);
               nrofpoints=8;
               d1=sqrt((x0-x01)^2+(y0-y01)^2+(z0-z01)^2);
               d2=sqrt((x0-x02)^2+(y0-y01)^2+(z0-z01)^2);
               d3=sqrt((x0-x01)^2+(y0-y02)^2+(z0-z01)^2);
               d4=sqrt((x0-x01)^2+(y0-y01)^2+(z0-z02)^2);
               d5=sqrt((x0-x01)^2+(y0-y02)^2+(z0-z02)^2);
               d6=sqrt((x0-x02)^2+(y0-y01)^2+(z0-z02)^2);
               d7=sqrt((x0-x02)^2+(y0-y02)^2+(z0-z02)^2);
               d8=sqrt((x0-x02)^2+(y0-y02)^2+(z0-z01)^2);
               if d1>1 || x01==x02
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x01,y01,z01);
               end
               if d2>1
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x02,y01,z01);
               end
               if d3>1 || y01==y02
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x01,y02,z01);
               end
               if d4>1 || z01==z02
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x01,y01,z02);
               end
               if d5>1
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x01,y02,z02);
               end
               if d6>1
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x02,y01,z02);
               end
               if d7>1
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x02,y02,z02);
               end
               if d8>1
                   nrofpoints=nrofpoints-1;
                   pointsimage(i,j)=pointsimage(i,j)-Imavol(x02,y02,z01);
               end
               pointsimage(i,j)=pointsimage(i,j)/nrofpoints;
           end
            
        end
    end
    end
end

pointsimage(all(~pointsimage,2),:)=[];
pointsimage(:,all(~pointsimage,1))=[];

InterpolatedImage=flipud(pointsimage);
end