# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:56:11 2022

@author: OQinYuan
"""

import numpy as np
from functions.wave_gen import write_to_txt, norm, reverse
from functions.read_files import _process_suffix, read_txt
from functions.wiener_deconvolution import \
    compare_wieners, test_wiener, get_best_wiener


def decon_tr_wiener(
    sig_h_path, lambd, output_path=None,
        write=False, snip=False):

    sig_h_path = _process_suffix(sig_h_path, '.txt')

    if output_path is None:
        output_path = f'{sig_h_path[:-4]}_decon_wiener.txt'

    sig_h = read_txt(sig_h_path)

    impulse_signal = np.zeros(sig_h.size)
    impulse_signal[0] = 1

    sig_h_decon = test_wiener(impulse_signal, sig_h, lambd=lambd, snip=snip)

    if write:
        data = reverse(norm(sig_h_decon))
        write_to_txt(output_path, data)


def decon_compare_wieners(sig_h_path, lambdas, logMode='plot'):

    sig_h_path = _process_suffix(sig_h_path, '.txt')

    sig_h = read_txt(sig_h_path)

    impulse_signal = np.zeros(sig_h.size)  # TODO abstract
    impulse_signal[0] = 1

    compare_wieners(impulse_signal, sig_h, lambdas, logMode=logMode)


def decon_get_best_wiener(sig_h_path, lambdas,
                          verbose=False,  write=False):
    """
    given an array of lambdas, assuming a singular maximum peak,
    find the lambda that produces the best temporal quality
    when unit impulse is deconvolved by given impulse response
    """

    sig_h_path = _process_suffix(sig_h_path, '.txt')

    sig_h = read_txt(sig_h_path)
    op_lambd = get_best_wiener(sig_h, lambdas, verbose=verbose)

    write and decon_tr_wiener(
        sig_h_path, op_lambd, write=True, snip=0)


if __name__ == '__main__':
    # make sure you run main_tr first to generate these files
    sig_h_args_list = [
        'oscilloscope/chirp/chirp1.Wfm_denoised_xcorr.txt',
        'oscilloscope/chirp/chirp3.Wfm_denoised_xcorr.txt'
    ]

    for sig_h_file_txt in sig_h_args_list:
        decon_get_best_wiener(
            sig_h_file_txt, np.linspace(0, 5, 101),
            verbose=True, write=1
        )
