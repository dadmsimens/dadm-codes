% Function for SoS (sum of squares) reconstruction
% INPUTS: 
%             data_simulated - data in each coil.       
%
% OUTPUTS:
%             data_reference_sos - data after SoS procedure.

function data_reference_sos = sos(data_simulated)
% reference image with noise
data_reference_sos = sqrt(sum(abs(data_simulated).^2, 3));
end 