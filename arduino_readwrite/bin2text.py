# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:30:04 2022

@author: OQinYuan
"""
# import numpy as np
from serial_read import write_to_bin_path

write_to_txt_path = "output_txt.txt"

with open(write_to_bin_path, "rb") as file:
    data = file.read()

array = list(map(int, data))


with open(write_to_txt_path, "w") as f:
    for d in array:
        val = (d / 512) - 1
        f.write('{:.4f} '.format(val))
