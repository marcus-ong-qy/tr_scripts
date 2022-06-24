# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:43:11 2022

@author: OQinYuan
"""

import numpy as np
from config import RATE
from wave_gen import show_fft, get_fft


def read_txt(filename):
    with open(f'{filename.replace(".txt", "")}.txt', 'r') as f:
        data_arr = f.read().split()
        data = np.array(list(map(float, list(data_arr))))

    return data


def get_fft_from_txt(
    filename, title=None, rate=RATE, xlim=None, ylim=None, show=False
):
    title = title if title else filename
    data = read_txt(filename)

    if show:
        x, y = show_fft(
            data, xlim=xlim, ylim=ylim, rate=rate, title=title
        )
    else:
        x, y = get_fft(
            data, xlim=xlim, ylim=ylim, rate=rate, title=title
        )

    return x, y


def fft_get_peak_freq(x, y):
    y_max = np.argmax(y)
    return x[y_max]


def data_analysis(txt_file, rate=RATE, xlim=None, ylim=None):

    x, y = get_fft_from_txt(
        txt_file, rate=rate, xlim=xlim, ylim=ylim, show=True
    )

    peak = fft_get_peak_freq(x, y)
    print('Peak Frequency:', peak, 'Hz')


if __name__ == '__main__':
    ANAL_PATH = 'oscilloscope/noisesamp/sensornoise3.Wfm'
    data_analysis(ANAL_PATH, xlim=[0, 200], ylim=[0, 25])

# x, y = get_fft_from_txt(
#     'arduino_readwrite/noise_samples/static_piezo_noise_15642', rate=15642)

# x, y = get_fft_from_txt(
#     'arduino_readwrite/noise_samples/static_piezo_noise_16915', rate=16915)

# x, y = get_fft_from_txt(
#     'arduino_readwrite/noise_samples/static_piezo_noise_16685', rate=16685)

# x, y = get_fft_from_txt(
#     'arduino_readwrite/noise_samples/static_piezo_noise_17620', rate=17620)

# x, y = get_fft_from_txt(
#     'arduino_readwrite/noise_samples/static_piezo_noise_17576', rate=17576)
