# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 17:00:11 2022

@author: OQinYuan
"""

import numpy as np


def ensure_filter_more_bigger_than_zero_everywhere(data, threshold=0.013):
    return np.array([n if abs(n) > threshold else threshold for n in data])
