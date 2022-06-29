# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:30:04 2022

@author: OQinYuan
"""
# import numpy as np
import struct
from serial_read import WRITE_TO_BIN_PATH

WRITE_TO_TXT_PATH = "chirp/13803_1"


def bin2text(path):
    '''
        Converts binary data from serial_read.py to Audacity
        Sample Data Import text file format \n

        You can use data_analysis.py to analyse FFT of the wave,
        or import to Audacity
    '''

    with open(WRITE_TO_BIN_PATH, "rb") as file:
        data = file.read()

        array = [
            struct.unpack('>H', data[i:i+2])[0] for i in range(0, len(data), 2)
        ]

        # # for i in range(0, len(data), 2):
        # #     info[i] = data[i, i+2]

        # array = struct.unpack("<H", data)
        # print(array)

    formatted_path = f'{path.replace(".txt", "")}.txt'

    with open(formatted_path, "w") as f:
        for d in array:
            # print(d)
            val = (d / 512) - 1
            f.write('{:.4f} '.format(val))

    print('Written to', formatted_path)


if __name__ == '__main__':
    bin2text(WRITE_TO_TXT_PATH)