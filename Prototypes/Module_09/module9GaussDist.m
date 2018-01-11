%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%        Function to create         %
%        Gauss distribution         %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function y = module9GaussDist(x,mu,v,p)

% x - column vector with non-zeros elemnts of histogram
% mu - column vector expected value of each clasters
% v - column vector of variation
% p - column vector of probability

mu = mu(:);
v = v(:);
p = p(:);

for i=1:size(mu,1)
   differ = x-mu(i);
   amplitude = p(i)/sqrt(2*pi*v(i)); 
   y(:,i) = amplitude*exp(-0.5 * (differ.*differ)/v(i));
end
