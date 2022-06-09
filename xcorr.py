# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:18:59 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal, fft
# from scipy.io.wavfile import read
from config import RATE, DURATION
from wave_gen import chirp,  plot, write_to_txt, norm, show_fft, get_fft, gauss_noise


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


time = np.arange(0, DURATION, 1/RATE)

# emitted signal s(t)
sig_s = chirp('lin', time, 2646, 2646, 1, 1, clipThreshold=0.5)
# sig_s = signal.unit_impulse(time.size, idx=0)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//4)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//2)
# sig_s = np.ones(time.size)

# impulse response h(t)
_t, sig_h = signal.impulse(([1], [26, 4, 6]), N=2646)


# detected signal r(t)
sig_r = signal.fftconvolve(sig_s, sig_h)
# sig_r += gauss_noise(sig_r.size)*0.0001

# Cross-correlation h(t)
sig_decon = signal.correlate(sig_r, sig_s)

sig_y = signal.convolve(sig_decon[::-1], sig_decon)


plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')
_, sig_sy = show_fft(sig_s, title="sig_s", xlim=[0, 2646])

plot(timeline(sig_h), sig_h, sample_sz=-1, title='sig_h h(t)')
_, sig_hy = show_fft(sig_h, title="sig_h", xlim=[0, 100])

plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
show_fft(sig_r, title="sig_r", xlim=[0, 2646])

# plot(timeline(sig_r_fmult), sig_r_fmult, sample_sz=-1, title='sig_r_fmult r(t)')
# show_fft(sig_r_fmult, title="sig_r_fmult", xlim=[0, 200])

plot(timeline(sig_decon),
     sig_decon, sample_sz=-1, title='sig_decon h(t)')
# show_fft(sig_decon, title="sig_decon")

# plot(timeline(sig_noise),
#      sig_noise, sample_sz=-1, title='sig_noise')


plot(timeline(sig_y),
     sig_y, sample_sz=-1, title='sig_y')
show_fft(sig_y, title="sig_y")

# write_to_txt('h', sig_h)
write_to_txt('s', norm(sig_s))
write_to_txt('r', norm(sig_r))
