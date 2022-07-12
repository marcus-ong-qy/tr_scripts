# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:45:07 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from scipy.fft import rfft, irfft
from config import RATE, DURATION
from fflip import fflip
from wave_gen import plot, write_to_txt, norm, show_fft, reverse as tr
from data_analysis import read_txt
from oscilloscope_read_csv_to_txt import _process_suffix, csv2txt


def timeline(amplitude):
    time = np.arange(0, DURATION, 1/RATE)
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


def decon_tr_fflip(
        chirp_path, sig_path, output_path=None,
        showPlot=False, log=False, reverse=True):

    chirp_path = _process_suffix(chirp_path, '.txt')
    sig_path = _process_suffix(sig_path, '.txt')

    if output_path is None:
        output_path = f'{sig_path[:-4]}_decon_tr.txt' if reverse  \
            else f'{sig_path[:-4]}_decon_tr.txt'

    # emitted signal s(t)
    sig_s = read_txt(chirp_path)

    # detected signal r(t)
    sig_r = read_txt(sig_path)

    # Cross-correlation h(t)
    sig_h = signal.correlate(sig_r, sig_s)
    log and print('\n\nsig_h:\n', sig_h)

    # fft of h(t), H(f)
    sig_h_fft = rfft(sig_h)
    log and print('\n\nsig_h_fft:\n', sig_h_fft)

    # inverse of H(f), H^(f)
    sig_h_fflipped = fflip(sig_h_fft, threshold=None)
    log and print('\n\nsig_h_fflipped:\n', sig_h_fflipped)

    # derived h(t)
    sig_h_decon = norm(irfft(sig_h_fflipped))
    log and print('\n\nsig_h_decon:\n', sig_h_decon)

    # sig_y = signal.convolve(sig_h[::-1], sig_h)

    if showPlot:
        plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')

        plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
        show_fft(sig_r, title="sig_r")

        plot(timeline(sig_h),
             sig_h, sample_sz=-1, title='sig_h h(t)')

        plot(timeline(sig_h_decon),
             sig_h_decon, sample_sz=-1, title='sig_h_decon h(t)')

    data = tr(sig_h_decon)  # if reverse else sig_h_decon

    write_to_txt(output_path, data)


if __name__ == '__main__':

    sig_file_txt = 'oscilloscope/chirp/chirp1.Wfm.txt'
    # noise_file_csv = 'oscilloscope/noisesamp/sensornoise1.Wfm.csv',
    chirp_file_txt = 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip0.7'

    decon_tr_fflip(chirp_file_txt, sig_file_txt,
                   showPlot=True, log=True, reverse=True)
