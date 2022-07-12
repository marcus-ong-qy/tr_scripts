# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 17:46:09 2022

@author: OQinYuan
"""

import numpy as np
from wave_gen import norm
from data_analysis import read_txt


def temporal_quality(data):
    """
    measures the temporal quality of the result, as detailed in 
    https://doi.org/10.1121/10.0009364, formula (4) (page 742)
    """
    data = norm(data)
    A_p = np.max(data)  # peak amplitude
    M = data.size  # number of samples

    sq_sum = 0  # sum of squares

    for val in data:
        sq_sum += val**2

    return A_p * np.sqrt(M/sq_sum)


def eval_temporal_quality(path):
    data = read_txt(path)
    et = temporal_quality(data)

    print('Temporal quality Report')
    print('for file:', path)
    print('E_T = ', data)


if __name__ == '__main__':
    paths = []
    for path in paths:
        eval_temporal_quality(path)
