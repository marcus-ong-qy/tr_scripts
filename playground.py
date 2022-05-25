# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:21:53 2022

@author: OQinYuan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from config import RATE, DURATION
from wave_gen import gauss_noise, chirp, plot, norm, write_to_txt


time = np.arange(0, DURATION, 1/RATE)

sig_mix = np.zeros(time.size)
# # C♯ minor chord
sig_mix += chirp('lin', time, 554.3653, 554.3653, 1, 1, clipThreshold=0.6)
sig_mix += chirp('lin', time, 659.2551, 659.2551, 1, 1, clipThreshold=0.8)
# sig_mix += chirp('lin', time, 830.6094, 830.6094, 1, 1, clipThreshold=1)
sig_mix += chirp('lin', time, 1108.731, 1108.731, 1, 1, clipThreshold=0.6)
sig_mix += gauss_noise(time)*0.1
sig_mix = norm(sig_mix)

plot(time, sig_mix, sample_sz=1000, title='sig_mix')

write_to_txt('fft', sig_mix)

# Number of samples in normalized_tone
N = int(RATE * DURATION)

yf = rfft(sig_mix)
xf = rfftfreq(N, 1 / RATE)

plt.plot(xf, np.abs(yf))
plt.show()
