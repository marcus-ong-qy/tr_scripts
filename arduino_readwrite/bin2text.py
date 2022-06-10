# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:30:04 2022

@author: OQinYuan
"""
# import numpy as np
from serial_read import WRITE_TO_BIN_PATH


def bin2text():
    '''
        Converts binary data from serial_read.py to Audacity
        Sample Data Import text file format \n

        You can use data_analysis.py to analyse FFT of the wave,
        or import to Audacity
    '''

    write_to_txt_path = "noise_samples/sample_17660_2.txt"

    with open(WRITE_TO_BIN_PATH, "rb") as file:
        data = file.read()

    array = list(map(int, data))

    with open(write_to_txt_path, "w") as f:
        for d in array:
            val = (d / 512) - 1
            f.write('{:.4f} '.format(val))


if __name__ == '__main__':
    bin2text()
