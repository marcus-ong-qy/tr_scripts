# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:21:53 2022

@author: OQinYuan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from config import RATE, DURATION
from wave_gen import chirp, plot, norm, write_to_txt


time = np.arange(0, DURATION, 1/RATE)

# C♯ minor chord
sig1 = chirp('lin', time, 554.3653, 554.3653, 1, 1, clipThreshold=1)
sig2 = chirp('lin', time, 659.2551, 659.2551, 1, 1, clipThreshold=1)
sig3 = chirp('lin', time, 830.6094, 830.6094, 1, 1, clipThreshold=1)
sig4 = chirp('lin', time, 1108.731, 1108.731, 1, 1, clipThreshold=1)
sig_mix = norm(sig1 + sig2 + sig3 + sig4)

plot(time, sig_mix, sample_sz=1000)

write_to_txt('fft', sig_mix)

# Number of samples in normalized_tone
N = RATE * DURATION

yf = rfft(sig_mix)
xf = rfftfreq(N, 1 / RATE)

plt.plot(xf, np.abs(yf))
plt.show()
