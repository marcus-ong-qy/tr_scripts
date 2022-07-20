# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:33:54 2022

@author: OQinYuan
"""

import numpy as np
from config import RATE, DURATION
from functions.remove_noise import remove_noise_csv
from functions.wave_gen import exp_chirp_and_inverse
from functions.xcorr import xcorr


def main_xcorr(sig_file_csv, noise_file_csv, chirp, inv_chirp,
               highpassCutoff=None, plot=False):
    sig_r = remove_noise_csv(sig_file_csv, noise_file_csv,
                             highpassCutoff=highpassCutoff,
                             plot=plot, write=False)
    xcorr_path = f'{sig_file_csv[:-4]}_denoised_xcorr.txt'
    xcorr(chirp, inv_chirp, sig_r,
          output_path=xcorr_path, showPlot=plot)


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
            'sig_file_csv': 'signal_data/response/rt1.Wfm.csv',
            'noise_file_csv': 'signal_data/noisesamp/sensornoise1.Wfm.csv',
            'chirp': chirp_data,
            'inv_chirp': inv
        },
        {
            'sig_file_csv': 'signal_data/response/rt3.Wfm.csv',
            'noise_file_csv': 'signal_data/noisesamp/sensornoise3.Wfm.csv',
            'chirp': chirp_data,
            'inv_chirp': inv
        },
    ]

    for args in args_list:
        main_xcorr(**args, highpassCutoff=2*f0, plot=1)
