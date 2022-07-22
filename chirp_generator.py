# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 17:23:28 2022

@author: OQinYuan
"""
import numpy as np
import config
from config import RATE, DURATION
from functions.wave_gen import chirp, write_to_txt, show_fft


time = np.arange(0, DURATION, 1/RATE)
amplitude = chirp('exp', time,
                  config.f0, config.f1, config.a0, config.a1,
                  )


show_fft(amplitude, title="chirp", xlim=[0, 2500], ylim=[0, 600])

PATH = 'signal_data/chirp/chirp_exp_' + \
    f'{DURATION}s_{config.f0}-{config.f1}_{config.a0}-{config.a1}'

write_to_txt(PATH, amplitude)
