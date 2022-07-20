# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:52:48 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from config import RATE, DURATION
from functions.wave_gen import chirp, plot, gauss_noise, show_fft


time = np.arange(0, DURATION, 1/RATE)
sig_s = chirp('lin', time, 500, 6000, 1, 1)
sig_h = chirp('lin', time, 6000, 500, 1, 1, clipThreshold=1)

sig_r = signal.convolve(sig_h, sig_s)
# sig_noise = gauss_noise(sig_r)*0.01
# sig_r += sig_noise

xcorr_h = signal.correlate(sig_s, sig_r)
# sig_y = signal.correlate(xcorr_h[::-1], xcorr_h)

decon_h, decon_noise = signal.deconvolve(sig_r[1:], sig_s[1:])
# decon_noise = norm(decon_noise)

plot(time[0:sig_s.size], sig_s, sample_sz=1000, title='sig_s')
plot(time[0:sig_h.size], sig_h, sample_sz=1000, title='sig_h')

plot(np.arange(0, DURATION*(sig_r.size/sig_s.size), 1/RATE),
     sig_r, sample_sz=1000, title='sig_r')

# plot(np.arange(0, DURATION*(sig_noise.size/sig_s.size), 1/RATE),
#      sig_noise, sample_sz=1000, title='sig_noise')

plot(np.arange(0, DURATION*(xcorr_h.size/sig_s.size), 1/RATE),
     xcorr_h, sample_sz=1000, title='xcorr_h')
show_fft(xcorr_h,  title='xcorr_h')
# plot(np.arange(0, DURATION*(sig_y.size/sig_s.size), 1/RATE),
#      sig_y, sample_sz=1000, title='sig_y')

plot(np.arange(0, DURATION*(decon_h.size/sig_s.size), 1/RATE),
     decon_h, sample_sz=1000, title='decon_h')
show_fft(decon_h,  title='decon_h')

# plot(np.arange(0, DURATION*(decon_noise.size/sig_s.size), 1/RATE), decon_noise,
#      sample_sz=1000, title='decon_noise')

# write_to_txt('sig_h', sig_h)
# write_to_txt('decon_h', decon_h)
