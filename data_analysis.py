# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:43:11 2022

@author: OQinYuan
"""

from config import RATE
from wave_gen import show_fft


def read_txt(filename):
    with open(f'{filename.replace(".txt", "")}.txt', 'r') as f:
        data_arr = f.read().split()
        data = list(map(float, list(data_arr)))

    return data


def _get_fft_from_txt(filename, rate=RATE):
    data = read_txt(filename)
    x, y = show_fft(data, xlim=[30, 50], ylim=[0, 2000], rate=rate)

    return x, y


x, y = _get_fft_from_txt(
    'arduino_readwrite/noise_samples/static_piezo_noise_15642', rate=15642)

x, y = _get_fft_from_txt(
    'arduino_readwrite/noise_samples/static_piezo_noise_16915', rate=16915)

x, y = _get_fft_from_txt(
    'arduino_readwrite/noise_samples/static_piezo_noise_16685', rate=16685)

x, y = _get_fft_from_txt(
    'arduino_readwrite/noise_samples/static_piezo_noise_17620', rate=17620)

x, y = _get_fft_from_txt(
    'arduino_readwrite/noise_samples/static_piezo_noise_17576', rate=17576)

# x, y = _get_fft_from_txt(
#     'arduino_readwrite/440_samples/sample_12771', rate=12771)
