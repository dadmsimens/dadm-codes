function [ data_output ] = normalize_data( data_input, EPSILON )
%NORMALIZE_DATA Summary of this function goes here
%   Detailed explanation goes here

minimum = min(min(min(data_input)));
maximum = max(max(max(data_input)));

data_output = EPSILON + (1-EPSILON)*(data_input - minimum)...
    /(maximum - minimum);


end

