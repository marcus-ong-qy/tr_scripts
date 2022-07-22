# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:33:54 2022

@author: OQinYuan
"""

import numpy as np
import config
from config import RATE, DURATION
from remove_noise import remove_noise_csv
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

    time = np.arange(0, DURATION, 1/RATE)
    chirp_data, inv = exp_chirp_and_inverse(
        time, config.f0, config.f1, config.a0, config.a1)

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
        main_xcorr(**args, highpassCutoff=2*config.f0, plot=0)
