# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:29:40 2022

@author: OQinYuan
"""

import numpy as np
from scipy.fft import rfft, rfftfreq, fft, fftfreq
from wave_gen import chirp, plot
from config import RATE, DURATION

time = np.arange(0, DURATION, 1/RATE)


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


const = np.ones(1000000)
const_fftfreq = rfft(const)

plot(timeline(const), const)
plot(timeline(const_fftfreq), const_fftfreq)
