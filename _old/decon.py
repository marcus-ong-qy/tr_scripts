# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
# from impulseest import impulseest
# import matplotlib.pyplot as plt
from scipy import signal
from data_analysis import read_txt
from functions.wave_gen import chirp, plot, show_fft, norm


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


# detected signal r(t)
sig_r = norm(read_txt(
    'arduino_readwrite/chirp/13803_1.txt'
))

RATE = 13803
DURATION = sig_r.size / RATE

time = np.arange(0, DURATION, 1/RATE)

# emitted signal s(t)
sig_s = chirp('exp', time, 100, 2000, 1, 1, clipThreshold=1)
# sig_s = signal.unit_impulse(time.size, idx=0)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//4)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//2)
# sig_s = np.ones(time.size)

# # impulse response h(t)
# _t, sig_h = signal.impulse(([1], [26, 4, 6]), N=2646)

# # hf_x, hf_y = get_fft(sig_h)
# # sig_h_inv = fft.irfft(hf_x)
# # sig_h_inv = norm(sig_h_inv)
# # sig_h_inv = sig_h_inv[::-1]

# sig_r = signal.fftconvolve(sig_s, sig_h)
# # sig_r += gauss_noise(sig_r.size)*0.0001

# Deconvolution h(t)
sig_decon, sig_noise = signal.deconvolve(
    sig_r, sig_s[1:] if sig_s[0] == 0 else sig_s)
# sig_decon = impulseest(sig_s, sig_r[0:sig_s.size])

# sig_y = signal.convolve(sig_decon[::-1], sig_decon)


plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
show_fft(sig_r, title="sig_r", xlim=[0, 2646], rate=RATE)


plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')
_, sig_sy = show_fft(sig_s, title="sig_s", xlim=[0, 2646], rate=RATE)

# plot(timeline(sig_h), sig_h, sample_sz=-1, title='sig_h h(t)')
# _, sig_hy = show_fft(sig_h, title="sig_h", xlim=[0, 100])

plot(timeline(sig_decon),
     sig_decon, sample_sz=-1, title='sig_decon h(t)')
# show_fft(sig_decon, title="sig_decon")

plot(timeline(sig_noise),
     sig_noise, sample_sz=-1, title='sig_noise')


# plot(timeline(sig_y),
#      sig_y, sample_sz=-1, title='sig_y')
# show_fft(sig_y, title="sig_y")

# # write_to_txt('h', sig_h)
# write_to_txt('s', norm(sig_s))
# write_to_txt('r', norm(sig_r))
