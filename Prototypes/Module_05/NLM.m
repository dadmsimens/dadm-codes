function [ output ]=NLM( image, Rsearch, Rsim, h )
 %input - image being filtered
 %Rsearch - radius of search window
 %Rsim - radius of the neighbourhood window
 %h - decay of exponential curve
 %
 %authors of algorithm: Jose V. Manjon & Antoni Buades
 %based on: "MRI denoising using Non-Local Means" by J. V. Manjon, J.
 %Carbonell-Caballero, J. J. Lull, G. Garcia-Marti, L. Marti-Bonmati, M.
 %Robles


 %size
 [m n]=size(image);

 %extend image at boundaries, to make calculations on edges possible
 input2 = padarray(image,[Rsim Rsim],'symmetric');
 
 %used kernel
 penalty = create_penalty(Rsim);
 penalty = penalty / sum(sum(penalty));
 
 h=h*h;
 
 for i=1:m %rows
 for j=1:n %columns
                 
         i1 = i+ Rsim; %extending image indexes
         j1 = j+ Rsim;        
         W1= input2(i1-Rsim:i1+Rsim , j1-Rsim:j1+Rsim);
         
         wmax=0; 
         average=0;
         sweight=0;
         
         rmin = max(i1-Rsearch,Rsim+1);
         rmax = min(i1+Rsearch,m+Rsim);
         smin = max(j1-Rsearch,Rsim+1);
         smax = min(j1+Rsearch,n+Rsim);
         
         for r=rmin:1:rmax %iterating inside neighbourhood
         for s=smin:1:smax
                                               
                if(r==i1 && s==j1) 
                    continue; %leaving central pixel
                end; 
                                
                W2= input2(r-Rsim:r+Rsim , s-Rsim:s+Rsim);                
                 
                d = sum(sum(penalty.*(W1-W2).*(W1-W2)));
                                               
                w=exp(-d/h);                 
                                 
                if w>wmax                
                    wmax=w;                   
                end
                
                sweight = sweight + w;
                average = average + w*input2(r,s);                                  
         end 
         end
             
        average = average + wmax*input2(i1,j1);
        sweight = sweight + wmax;
                   
        if sweight > 0
            output(i,j) = average / sweight;
        else
            output(i,j) = image(i,j);
        end                
 end
 end

        