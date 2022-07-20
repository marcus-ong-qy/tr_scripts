# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from config import RATE, DURATION
from functions.wave_gen import chirp,  plot, norm, show_fft, gauss_noise, clip, write_to_txt

time = np.arange(0, DURATION, 1/RATE)

# emitted signal s(t)
# sig_s = chirp('lin', time, 100, 2000, 1, 1, clipThreshold=0.7)
sig_s = signal.unit_impulse(time.size, idx=1)

# detected response r(t) (with noise)
sig_r = chirp('lin', time, 20, 10, 1, 1, clipThreshold=1)
# sig_r += gauss_noise(time)*0.5

# impulse response (?) h(t) = s(t) x r(t)
sig_ir = clip(norm(signal.correlate(sig_s, sig_r)), 1)

# Deconvolution TODO
sig_decon, sig_noise = signal.deconvolve(sig_r[1:], sig_s[1:])

# h(-t)
sig_tr = sig_ir[::-1]

# h(-t) * h(t) = y(t)
sig_y = signal.convolve(sig_ir, sig_tr)


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s')
show_fft(sig_s, title="sig_s")

plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r')
show_fft(sig_r, title="sig_r")

plot(timeline(sig_ir),
     sig_ir, sample_sz=-1, title='sig_ir h(t)')
show_fft(sig_ir, title="sig_ir")

plot(timeline(sig_tr),
     sig_tr, sample_sz=-1, title='sig_tr h(-t)')

plot(timeline(sig_decon),
     sig_decon, sample_sz=-1, title='sig_decon')
show_fft(sig_decon, title="sig_decon")

plot(timeline(sig_y),
     sig_y, sample_sz=-1, title='sig_y')
show_fft(sig_y, title="sig_y")

# plot(time, np.arange(0, DURATION*(len(sig_dec)/len(sig1))),
#       sample_sz=-1, title='sig_ir')
# write_to_txt('sig1', sig1)
# write_to_txt('sig2', sig2)
# write_to_txt('xcorr', sig_ir)
# write_to_txt('tr', sig_tr)
write_to_txt('y', norm(sig_y))
