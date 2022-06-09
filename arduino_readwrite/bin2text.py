# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:30:04 2022

@author: OQinYuan
"""
# import numpy as np
from serial_read import write_to_bin_path


def main():
    '''
        Converts binary data from serial_read.py to Audacity
        Sample Data Import text file format
    '''

    write_to_txt_path = "440_samples/sample_12771.txt"

    with open(write_to_bin_path, "rb") as file:
        data = file.read()

    array = list(map(int, data))

    with open(write_to_txt_path, "w") as f:
        for d in array:
            val = (d / 512) - 1
            f.write('{:.4f} '.format(val))


if __name__ == '__main__':
    main()
