# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:18:59 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from config import RATE, DURATION
from wave_gen import chirp,  plot, write_to_txt, norm, show_fft
from data_analysis import read_txt


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


time = np.arange(0, DURATION, 1/RATE)

# emitted signal s(t)
sig_s = chirp('exp', time, 100, 2000, 1, 1, clipThreshold=0.3)


# detected signal r(t)
sig_r = read_txt('oscilloscope/chirp/chirp3.Wfm_denoised.txt')

# Cross-correlation h(t)
sig_h = signal.correlate(sig_r, sig_s)

# sig_y = signal.convolve(sig_h[::-1], sig_h)


plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')

plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
show_fft(sig_r, title="sig_r", xlim=[0, 2646])

plot(timeline(sig_h),
     sig_h, sample_sz=-1, title='sig_h h(t)')
# show_fft(sig_h, title="sig_h")


write_to_txt('decon', norm(sig_h))
