# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 10:35:01 2022

@author: OQinYuan
"""
import numpy as np


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
