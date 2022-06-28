# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:33:54 2022

@author: OQinYuan
"""

import os
from oscilloscope_read_csv_to_txt import csv2txt
from remove_noise import remove_noise
# from data_analysis import data_analysis
from xcorr import xcorr
from decon_tr_fflip import decon_tr_fflip


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
    args_list = [
        {
            'sig_file_csv': 'oscilloscope/chirp/chirp1.Wfm.csv',
            'noise_file_csv': 'oscilloscope/noisesamp/sensornoise1.Wfm.csv',
            'chirp_file_txt': 'oscilloscope/chirp/chirp_exp_0.25s_100-2000_1-1_clip0.7'
        },
        # {
        #     'sig_file_csv': 'oscilloscope/chirp/chirp3.Wfm.csv',
        #     'noise_file_csv': 'oscilloscope/noisesamp/sensornoise3.Wfm.csv',
        #     'chirp_file_txt': 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip0.7'
        # }
    ]

    for args in args_list:
        main_xcorr(**args, plot=False)
        main_decon(**args, plot=True)
