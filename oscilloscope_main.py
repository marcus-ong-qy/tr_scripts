# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:33:54 2022

@author: OQinYuan
"""

import os
import numpy as np
from oscilloscope_read_csv_to_txt import csv2txt
from remove_noise import remove_noise
from xcorr import xcorr
from decon_tr_fflip import decon_tr_fflip
from wave_gen import exp_chirp_and_inverse
from config import RATE, DURATION
from inverse_filter import xcorr_more_better


def main_xcorr(sig_file_csv, noise_file_csv, chirp_file_txt, plot=False):
    sig_file_txt = csv2txt(sig_file_csv)
    noise_file_txt = csv2txt(noise_file_csv)

    sig_file_txt_denoised = f'{sig_file_txt[:-4]}_denoised.txt'
    if not os.path.exists(sig_file_txt_denoised):
        remove_noise(sig_file_txt, noise_file_txt, plot=plot)

    xcorr(chirp_file_txt, sig_file_txt, showPlot=plot, reverse=True)

    xcorr(chirp_file_txt, sig_file_txt_denoised, showPlot=plot, reverse=True)

    # data_analysis(txt_file_denoised, xlim=[0, 1000], ylim=[0, 200])


def main_decon(sig_file_csv, noise_file_csv, chirp_file_txt, plot=False):
    sig_file_txt = csv2txt(sig_file_csv)
    noise_file_txt = csv2txt(noise_file_csv)

    sig_file_txt_denoised = f'{sig_file_txt[:-4]}_denoised.txt'
    if not os.path.exists(sig_file_txt_denoised):
        remove_noise(sig_file_txt, noise_file_txt, plot=plot)

    decon_tr_fflip(chirp_file_txt, sig_file_txt,
                   showPlot=plot, reverse=True)
    decon_tr_fflip(chirp_file_txt, sig_file_txt_denoised,
                   showPlot=plot, reverse=True)

# data_analysis(txt_file_denoised, xlim=[0, 1000], ylim=[0, 200])


if __name__ == '__main__':
    '''
    ENSURE CONFIG FILE DATA CORRECT
    '''
    f0 = 100  # start frequency (Hz)
    f1 = 2000  # end frequency (Hz)
    a0 = 1  # start amplitude (normalised 0-1)
    a1 = 1  # end amplitude (normalised 0-1)
    clipThreshold = 1  # normalised 0-1

    time = np.arange(0, DURATION, 1/RATE)
    chirp_data, inv = exp_chirp_and_inverse(time, f0, f1, a0, a1)

    args_list = [
        {
            'sig_file_csv': 'oscilloscope/chirp/chirp1.Wfm.csv',
            'noise_file_csv': 'oscilloscope/noisesamp/sensornoise1.Wfm.csv',
            'chirp_file_txt': 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip1'
        },
        {
            'sig_file_csv': 'oscilloscope/chirp/chirp3.Wfm.csv',
            'noise_file_csv': 'oscilloscope/noisesamp/sensornoise3.Wfm.csv',
            'chirp_file_txt': 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip1'
        },
    ]

    more_better_signal_paths = [
        'oscilloscope/chirp/chirp1.Wfm_denoised.txt',
        'oscilloscope/chirp/chirp3.Wfm_denoised.txt'
    ]

    for args in args_list:
        main_xcorr(**args, plot=False)
        # main_decon(**args, plot=False)

    for path in more_better_signal_paths:
        xcorr_more_better(
            chirp_data, inv, path, showPlot=False)