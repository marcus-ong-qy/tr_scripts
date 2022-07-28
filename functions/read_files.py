# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:54:51 2022

@author: OQinYuan
"""

import csv
import numpy as np

CSV_FILE = 'signal_data/noisesamp/sensornoise3.Wfm.csv'


def _process_suffix(path, suffix):
    '''
    check if path entered has suffix, and adds suffix if there isn't\n
    e.g.:\n
        'text' -> 'text.txt'\n
        'text.txt' -> 'text.txt'
    '''
    return path if path.endswith(suffix) else f'{path}{suffix}'


def read_txt(filename):
    filename = _process_suffix(filename, '.txt')
    with open(filename, 'r') as f:
        data_arr = f.read().split()
        data = np.array(list(map(float, list(data_arr))))

    return data


def read_osc_csv(csv_file):
    """
    reads .Wfm.csv file from Rhode and Schwarz RTO1004 oscilloscope
    """
    csv_file = _process_suffix(csv_file, '.csv')

    data = []
    with open(csv_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            data.append(float(row[0]))
    return np.array(data)


def csv2txt(csv_file, txt_file=None):
    """
    converts .Wfm.csv file to Audacity-readable .txt file
    """
    csv_file = _process_suffix(csv_file, '.csv')

    if txt_file is None:
        txt_file = f'{csv_file[:-4]}.txt'

    with open(csv_file, newline='') as csvfile:
        with open(txt_file, 'w') as txtfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                txtfile.write('{:.4f} '.format(float(row[0])))

    return txt_file


if __name__ == '__main__':
    csv2txt(CSV_FILE)
