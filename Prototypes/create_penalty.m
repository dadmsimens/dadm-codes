function [penalty] = create_penalty(Rsim)              
 
penalty = zeros(2*Rsim+1,2*Rsim+1);   
for d = 1:Rsim    
  value = 1 / (2*d+1)^2 ;    
  for i = -d:d
  for j = -d:d
    penalty(Rsim+1-i,Rsim+1-j) = penalty(Rsim+1-i,Rsim+1-j) + value ;
  end
  end
end
penalty = penalty ./ Rsim;