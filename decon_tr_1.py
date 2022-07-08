# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:56:11 2022

@author: OQinYuan
"""

import numpy as np
from scipy import signal
from scipy.fft import rfft, irfft
from config import RATE, DURATION
from wave_gen import plot, write_to_txt, norm, show_fft, reverse
from data_analysis import read_txt
from oscilloscope_read_csv_to_txt import _process_suffix, csv2txt
from ensure_filter_more_bigger_than_zero_everywhere \
    import ensure_filter_more_bigger_than_zero_everywhere
from skimage import restoration
from wiener_deconvolution_example import compare_wieners, test_wiener


def timeline(amplitude):
    time = np.arange(0, DURATION, 1/RATE)
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)


def decon_tr(
        chirp_path, sig_path, output_path=None,
        showPlot=False, log=False):

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
    # sig_h += 1
    sig_h = ensure_filter_more_bigger_than_zero_everywhere(
        sig_h, threshold=0.001)
    log and print('\n\nsig_h:\n', sig_h)

    # if this is more longer my sig_h_decon spirals to infinity
    impulse_signal = np.zeros(sig_h.size)
    impulse_signal[0] = 1

    plot(timeline(rfft(impulse_signal)),
         rfft(impulse_signal), sample_sz=-1, title='impulse_signal')

    # inverse of H(f), H^(f)
    # sig_h_decon, _rem = signal.deconvolve(
    #     impulse_signal, sig_h)
    sig_h_decon, _rem = restoration.unsupervised_wiener(
        impulse_signal, sig_h)

    log and print('\n\nsig_h_decon:\n', sig_h_decon)
    log and print('\n\n_rem:\n', _rem)

    if showPlot:
        plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')

        plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')
        show_fft(sig_r, title="sig_r")

        plot(timeline(sig_h),
             sig_h, sample_sz=-1, title='sig_h h(t)')

        plot(timeline(sig_h_decon),
             sig_h_decon, sample_sz=-1, title='sig_h_decon h(t)')

        plot(timeline(_rem),
             _rem, sample_sz=-1, title='_rem')

    data = reverse(sig_h_decon)
    write_to_txt(output_path, data)

def decon_tr_wiener(chirp_path, sig_path, output_path=None, log=False, write=False):

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
    impulse_signal[0] = 1

    sig_h_decon = test_wiener(impulse_signal, sig_h, lambd=7.03e-4)

    if write:
        data = reverse(sig_h_decon)
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
    impulse_signal[0] = 1

    compare_wieners(impulse_signal, sig_h, lambdas)

if __name__ == '__main__':
    sig_file_txt = 'oscilloscope/chirp/chirp1.Wfm.txt'
    # noise_file_csv = 'oscilloscope/noisesamp/sensornoise1.Wfm.csv',
    chirp_file_txt = 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip1'

    # decon_tr(chirp_file_txt, sig_file_txt, showPlot=True, log=True)

    # decon_tr_wiener(chirp_file_txt, sig_file_txt, log=True, write=False)

    decon_compare_wieners(chirp_file_txt, sig_file_txt, [
        8e-4, 
        7.03e-4,
        7e-4,
        6e-4,
    ])
