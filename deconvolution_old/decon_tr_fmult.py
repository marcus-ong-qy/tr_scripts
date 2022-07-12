# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
from config import RATE, DURATION
from wave_gen import chirp,  plot, write_to_txt, norm, show_fft, get_fft, \
    gauss_noise, show_fft_cmplx


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


time = np.arange(0, DURATION, 1/RATE)

# emitted signal s(t)
sig_s = chirp('lin', time, 264.6, 2646, 1, 1, clipThreshold=1)
# sig_s = signal.unit_impulse(time.size, idx=1)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//4)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//2)
# sig_s = np.ones(time.size)
# sig_s += gauss_noise(time)*0.01

# impulse response h(t)
_t, sig_h = signal.impulse(([1.0], [1.0, 2.0, 1.0]), N=time.size)

# hf_x, hf_y = get_fft(sig_h)
# sig_h_inv = fft.irfft(hf_x)
# sig_h_inv = norm(sig_h_inv)
# sig_h_inv = sig_h_inv[::-1]


# detected signal r(t)
fft_s = fft.rfft(sig_s)
fft_h = fft.rfft(sig_h)
sig_r = fft.irfft(fft_s * fft_h)


# Deconvolution h(t)
sig_decon, sig_noise = signal.deconvolve(sig_r[1:], sig_s[1:])

# sig_y = signal.convolve(sig_ir, sig_tr)


plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')
show_fft(sig_s, title="sig_s", xlim=[0, 5000])

plot(timeline(sig_h), sig_h, sample_sz=-1, title='sig_h h(t)')
show_fft(sig_h, title="sig_h", xlim=[0, 10])

plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
show_fft_cmplx(sig_r, title="sig_r", xlim=[0, 5000])

plot(timeline(sig_decon),
     sig_decon, sample_sz=-1, title='sig_decon h(t)')
# show_fft(sig_decon, title="sig_decon")

plot(timeline(sig_noise),
     sig_noise, sample_sz=-1, title='sig_noise')


# plot(timeline(sig_h_inv),
#      sig_h_inv, sample_sz=-1, title='sig_h_inv "broadcast to system"')
# # show_fft(sig_h_inv, title="sig_h_inv")

# write_to_txt('h', sig_h)
write_to_txt('r', norm(sig_r))
