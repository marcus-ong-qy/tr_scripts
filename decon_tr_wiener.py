# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:56:11 2022

@author: OQinYuan
"""

import numpy as np

from wave_gen import write_to_txt, norm, reverse
from data_analysis import read_txt
from oscilloscope_read_csv_to_txt import _process_suffix
from _wiener_deconvolution_example import compare_wieners, test_wiener


def decon_tr_wiener(
        chirp_path, sig_h_path, lambd, output_path=None,
        log=False, write=False, snip=False):

    chirp_path = _process_suffix(chirp_path, '.txt')
    sig_h_path = _process_suffix(sig_h_path, '.txt')

    if output_path is None:
        output_path = f'{sig_h_path[:-4]}_decon_wiener.txt'

    sig_h = read_txt(sig_h_path)

    impulse_signal = np.zeros(sig_h.size)
    for i in range(1):
        impulse_signal[i] = 1

    sig_h_decon = test_wiener(impulse_signal, sig_h, lambd=lambd, snip=snip)

    if write:
        # TODO implement Audacity's Normalize instead
        data = reverse(norm(sig_h_decon))
        write_to_txt(output_path, data)


def decon_compare_wieners(chirp_path, sig_h_path, lambdas):

    chirp_path = _process_suffix(chirp_path, '.txt')
    sig_h_path = _process_suffix(sig_h_path, '.txt')

    sig_h = read_txt(sig_h_path)

    impulse_signal = np.zeros(sig_h.size)
    for i in range(1):
        impulse_signal[i] = 1

    compare_wieners(impulse_signal, sig_h, lambdas)


if __name__ == '__main__':
    chirp_file_txt = 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip1'

    sig_h_args_list = [
        # 'oscilloscope/chirp/chirp1.Wfm_denoised_xcorr',
        'oscilloscope/chirp/chirp3.Wfm_denoised_xcorr'
    ]

    for sig_h_file_txt in sig_h_args_list:
        # decon_tr_wiener(
        #     chirp_file_txt, sig_h_file_txt, 3.5, log=True, write=1, snip=0)

        decon_compare_wieners(chirp_file_txt, sig_h_file_txt, [
            3.3,
            3.5,
            3.7,
        ])
