# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:23:28 2022

@author: OQinYuan
"""
import numpy as np
from config import RATE, DURATION
from wave_gen import chirp, write_to_txt

type_ = 'exp'
f0 = 100
f1 = 4000
a0 = 1
a1 = 1
# clip_thresh = 0.7 ## NOT SUPPOSED TO CLIP


time = np.arange(0, DURATION, 1/RATE)
amplitude = chirp(type_, time,
                  f0, f1, a0, a1,
                  # clipThreshold=clip_thresh
                  )

PATH = f'oscilloscope/chirp/chirp_{type_}_{DURATION}s_{f0}-{f1}_{a0}-{a1}'


write_to_txt(PATH, amplitude)
