clc; close all; clear all

data = read_txt('chirp1.Wfm_denoised_xcorr_more_better.txt');
data = cell2mat(data);
sz = size(data);
sz = sz(1);
impulse = zeros([sz 1]);
impulse(1) = 1;

[t,w] = deconvolution(impulse,data);   

plot(t,w)


function C=read_txt(filename)
    
    fid = fopen(filename,'rt');
    C = textscan(fid, '%f');
    fclose(fid);
end
    