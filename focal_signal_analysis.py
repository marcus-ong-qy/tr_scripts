# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:46:09 2022

@author: OQinYuan
"""

import config
from config import DURATION, RATE
import numpy as np
from functions.wave_gen import plot, timeline
from functions.temporal_quality import temporal_quality
from remove_noise import remove_noise_csv


def energy(data):
    sq_sum = np.sum(np.abs(data)**2)
    return sq_sum * DURATION/RATE


def focal_signal_analysis(path_file_csv, noise_file_csv,
                          highpassCutoff=None):
    """
    input the path file for the focus signal, and the noise file\n
    Output log glossary: \n
    Peak: amplitude of the peak \n
    E_T: the Temporal Quality of the signal \n
    Energy: the energy of the signal \n
    What is Temporal Quality?:
    measures the temporal quality of the result, as detailed in
    https://doi.org/10.1121/10.0009364, formula (4) (page 742)
    """

    data = remove_noise_csv(
        path_file_csv, noise_file_csv, highpassCutoff=highpassCutoff,
        write=False, plot=False)

    peak, et = temporal_quality(data)

    print()
    print('===')
    print('Temporal quality Report')
    print('for file:', path_file_csv)
    print('Peak:', peak)
    print('E_T:', et)
    print('Energy:', "{:e}".format(energy(data)))
    print('===')
    print()

    time = timeline(data)
    plot(time, data)


if __name__ == '__main__':
    HIGHPASS_CUTOFF = config.f0 * 2
    args = [
        {
            'path_file_csv': 'signal_data/focus/focus1_trad.Wfm.csv',
            'noise_file_csv': 'signal_data/noisesamp/sensornoise1.Wfm.csv'
        },
        {
            'path_file_csv': 'signal_data/focus/focus1_decon.Wfm.csv',
            'noise_file_csv': 'signal_data/noisesamp/sensornoise1.Wfm.csv'
        },
        {
            'path_file_csv': 'signal_data/focus/focus3_trad.Wfm.csv',
            'noise_file_csv': 'signal_data/noisesamp/sensornoise3.Wfm.csv'
        },
        {
            'path_file_csv': 'signal_data/focus/focus3_decon.Wfm.csv',
            'noise_file_csv': 'signal_data/noisesamp/sensornoise3.Wfm.csv'
        },
    ]

    # args = [
    #     {
    #         'path_file_csv': 'signal_data/Response Samples/focus1.Wfm.csv',
    #         'noise_file_csv': 'signal_data/noisesamp/sensornoise1.Wfm.csv'
    #     },
    #     {
    #         'path_file_csv': 'signal_data/Response Samples/non_focus1.Wfm.csv',
    #         'noise_file_csv': 'signal_data/noisesamp/sensornoise1.Wfm.csv'
    #     },
    #     {
    #         'path_file_csv': 'signal_data/Response Samples/focus3.Wfm.csv',
    #         'noise_file_csv': 'signal_data/noisesamp/sensornoise3.Wfm.csv'
    #     },
    #     {
    #         'path_file_csv': 'signal_data/Response Samples/non_focus3.Wfm.csv',
    #         'noise_file_csv': 'signal_data/noisesamp/sensornoise3.Wfm.csv'
    #     },
    # ]

    # args = [
    #     {
    #         'path_file_csv': 'signal_data/clipOrNoClip/noclip.Wfm.csv',
    #         'noise_file_csv': 'signal_data/noisesamp/sensornoise1.Wfm.csv'
    #     },
    #     {
    #         'path_file_csv': 'signal_data/clipOrNoClip/yesclip.Wfm.csv',
    #         'noise_file_csv': 'signal_data/noisesamp/sensornoise1.Wfm.csv'
    #     },
    # ]

    for kwargs in args:
        focal_signal_analysis(**kwargs, highpassCutoff=HIGHPASS_CUTOFF)
