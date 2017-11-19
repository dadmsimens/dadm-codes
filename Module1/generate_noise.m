% Function for creating additive noise to sampled data
% normally distributed noise in each coil in x-space domain 
% INPUTS: 
%             std=const.(chosen standard deviation),
%             image - the size of the image defines the size of noise,
%             n_coils - number of coils
%
% OUTPUTS:
%         noise - new random noise is generated for each coil

function noise = generate_noise(std, image, n_coils, rho)
    
    if(rho == 0) 
        Int=It+sigma.*(randn(size(It))+j.*randn(size(It)));        
    else
        % covariance matrix
    
        noise = random('Normal', 0, std, [size(image), n_coils]) + 1i.*random('Normal', 0, std, [size(image), n_coils]);
    end
end
