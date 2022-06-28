# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:18:59 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from config import RATE, DURATION
from wave_gen import chirp, plot, write_to_txt, norm, show_fft, reverse as tr
from data_analysis import read_txt
from oscilloscope_read_csv_to_txt import _process_suffix


time = np.arange(0, DURATION, 1/RATE)


def timeline(amplitude):
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


READ_PATH = 'oscilloscope/chirp/chirp3.Wfm_denoised.txt'
CHIRP_SIG = chirp('exp', time, 100, 2000, 1, 1, clipThreshold=0.3)


def xcorr(chirp_path, sig_path, output_path=None, showPlot=False, reverse=False):

    chirp_path = _process_suffix(chirp_path, '.txt')
    sig_path = _process_suffix(sig_path, '.txt')

    if output_path is None:
        output_path = f'{sig_path[:-4]}_xcorr_tr.txt' if reverse  \
            else f'{sig_path[:-4]}_xcorr.txt'

    # emitted signal s(t)
    sig_s = read_txt(chirp_path)

    # detected signal r(t)
    sig_r = read_txt(sig_path)

    # Cross-correlation h(t)
    sig_h = signal.correlate(sig_r, sig_s)

    # sig_y = signal.convolve(sig_h[::-1], sig_h)

    if showPlot:
        plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')

        plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
        show_fft(sig_r, title="sig_r")

        plot(timeline(sig_h),
             sig_h, sample_sz=-1, title='sig_h h(t)')
        # show_fft(sig_h, title="sig_h")

    data = tr(norm(sig_h)) if reverse else norm(sig_h)

    write_to_txt(output_path, data)


if __name__ == '__main__':
    xcorr(READ_PATH)
