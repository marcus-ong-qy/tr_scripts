# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
import scipy.signal
# from config import RATE, DURATION
from wave_gen import chirp, write_to_txt, plot, norm

RATE = 1000
DURATION = 1

time = np.arange(0, DURATION, 1/RATE)
sig1 = chirp('lin', time, 10, 20, 1, 1)
sig2 = chirp('hyp', time, 26, 46, 1, 1, clipThreshold=1)

sig_ir = norm(scipy.signal.correlate(sig1, sig2))
sig_dec = scipy.signal.deconvolve(sig1[1:], sig2[1:])
sig_tr = sig_ir[::-1]

plot(time, sig1, sample_sz=-1, title='sig1')
plot(time, sig2, sample_sz=-1, title='sig2')
plot(time, sig_ir, sample_sz=-1, title='sig_ir')
plot(time, np.arange(0, DURATION*(len(sig_dec)/len(sig1))),
     sample_sz=-1, title='sig_ir')
# write_to_txt('sig1', sig1)
# write_to_txt('sig2', sig2)
# write_to_txt('xcorr', sig_ir)
# write_to_txt('tr', sig_tr)
