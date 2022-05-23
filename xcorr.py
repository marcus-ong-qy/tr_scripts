# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
import scipy.signal
from wave_gen import chirp, write_to_txt

RATE = 44100  # sampling rate in Hz
DURATION = 0.5  # duration of signal, in seconds

time = np.arange(0, DURATION, 1/RATE)
sig1 = chirp('lin', time, 100, 2000, 1, 1)
sig2 = chirp('lin', time, 264, 600, 1, 1)

sig_corr = scipy.signal.correlate(sig1, sig2)

write_to_txt('sig1', sig1)
write_to_txt('sig2', sig2)
write_to_txt('xcorr', sig_corr)
