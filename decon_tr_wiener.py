# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:56:11 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from config import RATE, DURATION
from wave_gen import write_to_txt, norm
from data_analysis import read_txt
from oscilloscope_read_csv_to_txt import _process_suffix
from ensure_filter_more_bigger_than_zero_everywhere \
    import ensure_filter_more_bigger_than_zero_everywhere
from wiener_deconvolution_example import compare_wieners, test_wiener


def timeline(amplitude):
    time = np.arange(0, DURATION, 1/RATE)
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


def decon_tr_wiener(
        chirp_path, sig_path, output_path=None, log=False, write=False):

    chirp_path = _process_suffix(chirp_path, '.txt')
    sig_path = _process_suffix(sig_path, '.txt')

    if output_path is None:
        output_path = f'{sig_path[:-4]}_decon_tr.txt'

    # emitted signal s(t)
    sig_s = read_txt(chirp_path)

    # detected signal r(t)
    sig_r = read_txt(sig_path)

    # Cross-correlation h(t)
    sig_h = signal.correlate(sig_r, sig_s)
    # sig_h = np.pad(sig_h, (sig_h.size, sig_h.size))
    sig_h = ensure_filter_more_bigger_than_zero_everywhere(
        sig_h, threshold=0.001)
    log and print('\n\nsig_h:\n', sig_h)

    # # if this is more longer my sig_h_decon spirals to infinity
    impulse_signal = np.zeros(sig_h.size)
    for i in range(1):
        impulse_signal[i] = 1

    sig_h_decon = test_wiener(impulse_signal, sig_h, lambd=0.5e3)
    log and print('\n\nsig_h_decon:\n', sig_h_decon)

    if write:
        data = norm(sig_h_decon)
        write_to_txt(output_path, data)


def decon_compare_wieners(chirp_path, sig_path, lambdas):

    chirp_path = _process_suffix(chirp_path, '.txt')
    sig_path = _process_suffix(sig_path, '.txt')

    # emitted signal s(t)
    sig_s = read_txt(chirp_path)

    # detected signal r(t)
    sig_r = read_txt(sig_path)

    # Cross-correlation h(t)
    sig_h = signal.correlate(sig_r, sig_s)
    # sig_h = np.pad(sig_h, (sig_h.size, sig_h.size))
    sig_h = ensure_filter_more_bigger_than_zero_everywhere(
        sig_h, threshold=0.001)

    # # if this is more longer my sig_h_decon spirals to infinity
    impulse_signal = np.zeros(sig_h.size)
    for i in range(1):
        impulse_signal[i] = 1

    compare_wieners(impulse_signal, sig_h, lambdas)


if __name__ == '__main__':
    chirp_file_txt = 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip1'

    sig_args_list = [
        'oscilloscope/chirp/chirp1.Wfm.txt',
        'oscilloscope/chirp/chirp2.Wfm.txt'
    ]

    for sig_file_txt in sig_args_list:
        decon_tr_wiener(chirp_file_txt, sig_file_txt, log=True, write=True)

        # decon_compare_wieners(chirp_file_txt, sig_file_txt, [
        #     1e-0,
        #     0.5e3,
        #     1e2,
        # ])
