# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
import scipy.signal
from config import RATE, DURATION
from wave_gen import chirp, write_to_txt

time = np.arange(0, DURATION, 1/RATE)
sig1 = chirp('lin', time, 100, 2000, 1, 1)
sig2 = chirp('hyp', time, 264, 600, 1, 1, waveType="square")

sig_ir = scipy.signal.correlate(sig1, sig2)
sig_tr = sig_ir[::-1]

write_to_txt('sig1', sig1)
write_to_txt('sig2', sig2)
write_to_txt('xcorr', sig_ir)
write_to_txt('tr', sig_tr)
