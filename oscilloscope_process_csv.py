# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 09:33:54 2022

@author: OQinYuan
"""

from oscilloscope_read_csv_to_txt import csv2txt
from remove_noise import remove_noise
from data_analysis import data_analysis

CSV_FILE = 'oscilloscope/chirp/chirp3_clip.Wfm'
NOISE_SAMPLE = 'oscilloscope/noisesamp/sensornoise3.Wfm.txt'

txt_file = csv2txt(CSV_FILE)
txt_file_denoised = remove_noise(txt_file, NOISE_SAMPLE, plot=True)

data_analysis(txt_file_denoised, xlim=[0, 1000], ylim=[0, 200])
