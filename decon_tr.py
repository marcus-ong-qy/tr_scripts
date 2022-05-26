# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from config import RATE, DURATION
from wave_gen import chirp,  plot, show_fft, write_to_txt

time = np.arange(0, DURATION, 1/RATE)

# emitted signal s(t)
# sig_s = chirp('lin', time, 100, 2000, 1, 1, clipThreshold=0.7)
sig_s = signal.unit_impulse(time.size, idx=0)/2 + \
    signal.unit_impulse(time.size, idx=time.size//4)/2 + \
    signal.unit_impulse(time.size, idx=time.size//2)

# h(t)
sig_h = chirp('lin', time, 1000, 800, 1, 0, clipThreshold=0.7)

sig_r = signal.convolve(sig_s, sig_h)

# Deconvolution h(t)
sig_decon, sig_noise = signal.deconvolve(sig_r, sig_s)

# sig_y = signal.convolve(sig_ir, sig_tr)


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s')
# show_fft(sig_s, title="sig_s")

plot(timeline(sig_h), sig_h, sample_sz=-1, title='sig_h')
# show_fft(sig_h, title="sig_h")

plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r')
# show_fft(sig_r, title="sig_r")

plot(timeline(sig_decon),
     sig_decon, sample_sz=-1, title='sig_decon h(t)')
# show_fft(sig_decon, title="sig_decon")

plot(timeline(sig_noise),
     sig_noise, sample_sz=-1, title='sig_noise')

write_to_txt('h', sig_h)
write_to_txt('r', sig_r)
