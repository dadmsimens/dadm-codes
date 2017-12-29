function [ data_output ] = normalize_data( dwi, EPSILON )
%NORMALIZE_DATA Summary of this function goes here
%   Detailed explanation goes here

minimum = min(min(min(dwi.data)));
maximum = max(max(max(dwi.data)));

if maximum - minimum ~= 0
    data_output = EPSILON + (1-EPSILON)*(dwi.data - minimum)...
        /(maximum - minimum);
else
    data_output = dwi.data;
end

end

