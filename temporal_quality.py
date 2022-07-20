# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:46:09 2022

@author: OQinYuan
"""

import numpy as np
from functions.wave_gen import plot, timeline
from functions.remove_noise import remove_noise_csv


def temporal_quality(data):
    """
    measures the temporal quality of the result, as detailed in
    https://doi.org/10.1121/10.0009364, formula (4) (page 742)
    """
    A_p = np.max(data)  # peak amplitude
    M = data.size  # number of samples

    sq_sum = 0  # sum of squares

    for val in data:
        sq_sum += val**2

    e_t = A_p * np.sqrt(M/sq_sum)

    return A_p, e_t


def eval_temporal_quality(path_file_csv, noise_file_csv, highpassCutoff=None):
    """
    input the path file for the focus signal, and the noise file\n
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
    print('===')
    print()

    time = timeline(data)
    plot(time, data)


if __name__ == '__main__':
    args = [
        {
            'path_file_csv': 'oscilloscope/foci/focus1_trad.Wfm.csv',
            'noise_file_csv': 'oscilloscope/noisesamp/sensornoise1.Wfm.csv'
        },
        {
            'path_file_csv': 'oscilloscope/foci/focus1_decon.Wfm.csv',
            'noise_file_csv': 'oscilloscope/noisesamp/sensornoise1.Wfm.csv'
        },
        {
            'path_file_csv': 'oscilloscope/foci/focus3_trad.Wfm.csv',
            'noise_file_csv': 'oscilloscope/noisesamp/sensornoise3.Wfm.csv'
        },
        {
            'path_file_csv': 'oscilloscope/foci/focus3_decon.Wfm.csv',
            'noise_file_csv': 'oscilloscope/noisesamp/sensornoise3.Wfm.csv'
        },
    ]

    for kwargs in args:
        eval_temporal_quality(**kwargs, highpassCutoff=200)
