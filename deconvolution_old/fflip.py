# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 12:09:28 2022

@author: OQinYuan
"""

import numpy as np


def fflip(amplitude, threshold=None):
    if threshold is None:
        threshold = np.amax(amplitude)

    lim_l = 1/threshold

    output = np.zeros(amplitude.size)

    for i, val in enumerate(amplitude):
        output[i] = threshold if val < lim_l else 1/val

    return output


if __name__ == '__main__':
    array = np.array([2, 6, 4, 6, 0, 0.0001])
    print(fflip(array))
