# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
from config import RATE, DURATION
from functions.wave_gen import chirp,  plot, write_to_txt, norm, show_fft, get_fft, gauss_noise
from data_analysis import read_txt


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


time = np.arange(0, DURATION, 1/RATE)

# emitted signal s(t)
sig_s = chirp('exp', time, 100, 2000, 1, 1, clipThreshold=1)
# sig_s = signal.unit_impulse(time.size, idx=0)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//4)/2 + \
#     signal.unit_impulse(time.size, idx=time.size//2)
# sig_s = np.ones(time.size)
# sig_s += gauss_noise(time)*0.01

# impulse response h(t)
# _t, sig_h = signal.impulse(([1.0], [1.0, 2.0, 1.0]), N=time.size)
# sig_h = read_txt('oscilloscope/chirp/chirp1.Wfm_denoised.txt')

# hf_x, hf_y = get_fft(sig_h)
# sig_h_inv = fft.irfft(hf_x)
# sig_h_inv = norm(sig_h_inv)
# sig_h_inv = sig_h_inv[::-1]


# detected signal r(t)
# sig_r = np.convolve(sig_s, sig_h)
sig_r = read_txt('oscilloscope/chirp/chirp1.Wfm_denoised.txt')

# Sig_h = fft.fft(sig_h)
# f_axis = fft.fftfreq(Sig_h.size, 1/RATE)
# freq_idx = np.argmin(np.abs(f_axis - 100))
# print(Sig_h[freq_idx])
# plt.plot(f_axis, np.abs(Sig_h))
# plt.grid()
# plt.xlim([0, 200])
# plt.show()

# sig_r_fmult = fft.fft(sig_s) * fft.fft(sig_h)
# sig_r_fmult_x = fft.fftfreq(sig_r_fmult.size, 1/RATE)
# plt.plot(sig_r_fmult_x, np.abs(sig_r_fmult))
# plt.xlim([0, 200])
# plt.show()

# Deconvolution h(t)
sig_decon, sig_noise = signal.deconvolve(sig_r[1:], sig_s[1:])

# sig_y = signal.convolve(sig_ir, sig_tr)


plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')
show_fft(sig_s, title="sig_s", xlim=[0, 3000])

# plot(timeline(sig_h), sig_h, sample_sz=-1, title='sig_h h(t)')
# show_fft(sig_h, title="sig_h", xlim=[0, 10])

plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
show_fft(sig_r, title="sig_r", xlim=[0, 3000])

# plot(timeline(sig_r_fmult), sig_r_fmult, sample_sz=-1, title='sig_r_fmult r(t)')
# show_fft(sig_r_fmult, title="sig_r_fmult", xlim=[0, 200])

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
