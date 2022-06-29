# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:53:42 2022

@author: OQinYuan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq
# import random
from config import RATE, DURATION


def lin_amp_grad(time, a0, a1):
    if a0 == a1:
        return np.ones(time.size) * a0

    return np.arange(a0, a1, (a1-a0)/time.size)


def lin_chirp(time, f0, f1, a0, a1):
    c = (f1-f0)/DURATION
    a = lin_amp_grad(time, a0, a1)
    x = np.sin(
        2 * np.pi * (
            ((c/2) * time**2) + f0 * time
        )
    )
    return np.multiply(a, x)


def exp_chirp(time, f0, f1, a0, a1):
    k = ((f1/f0)**(1/DURATION))
    a = lin_amp_grad(time, a0, a1)
    x = np.sin(
        2 * np.pi * f0 * (
            (k**time - 1) / np.log(k)
        )
    )
    return np.multiply(a, x)


def exp_chirp_and_inverse(time, f0, f1, a0, a1):
    k = ((f1/f0)**(1/DURATION))
    a = lin_amp_grad(time, a0, a1)
    x = np.sin(
        2 * np.pi * f0 * (
            (k**time - 1) / np.log(k)
        )
    )
    chirp = np.multiply(a, x)

    R = np.log(f1/f0)

    # Inverse filter
    k_inv = np.exp(time*R/DURATION)
    inv = chirp[::-1]/k_inv

    return chirp, inv


def hyp_chirp(time, f0, f1, a0, a1):
    a = lin_amp_grad(time, a0, a1)
    x = np.sin(
        2 * np.pi * (
            (-f0 * f1 * DURATION) / (f1 - f0)
        ) * np.log(
            1 - ((f1 - f0) / (f1 * DURATION)) * time
        )
    )
    return np.multiply(a, x)


def square(wave):
    output = np.zeros(wave.size)
    for i in range(output.size):
        output[i] = 1 if wave[i] >= 0 else -1
    return output


def clip(wave, threshold):
    if threshold >= 1:
        return wave
    if threshold == 0:
        return square(wave)

    output = np.zeros(wave.size)
    for i in range(output.size):
        if wave[i] >= threshold:
            output[i] = 1
        elif wave[i] <= -threshold:
            output[i] = -1
        else:
            output[i] = wave[i]/threshold
    return output


def reverse(wave):
    if type(wave) == np.ndarray:
        return np.flip(wave)

    return wave[::-1]


def norm(wave, symmetric=False):
    if symmetric:
        return wave/np.abs(wave).max()

    max_pt = wave.max()
    min_pt = wave.min()
    mid = (max_pt + min_pt)/2
    amp = (max_pt - min_pt)/2

    return (wave-mid)/amp


def chirp(waveFn, time, f0, f1, a0, a1,  clipThreshold=1):
    """
        waveFn: 'lin' (default), 'exp', 'hyp' \n
        time: array of time axis values \n
        f0: start frequency (Hz) \n
        f1: end frequency (Hz) \n
        a0: start amplitude (normalised 0-1) \n
        a1: end amplitude (normalised 0-1) \n
        clipThreshold: normalised 0-1
    """
    if waveFn == 'exp':
        wave = exp_chirp(time, f0, f1, a0, a1)
    elif waveFn == 'hyp':
        wave = hyp_chirp(time, f0, f1, a0, a1)
    else:
        wave = lin_chirp(time, f0, f1, a0, a1)

    return clip(wave, clipThreshold)


def gauss_noise(size):
    return np.random.normal(0, 1, size)


def plot(time, amplitude, sample_sz=-1, title='Wave'):
    '''
    sample_sz: number of data points to plot (default -1 plots whole waveform)
    '''
    # Plot a sine wave using time and amplitude obtained for the sine wave
    size = time.size if isinstance(
        time, np.ndarray) else len(time)

    sz = size if sample_sz == -1 else min(sample_sz, size)
    plt.plot(time[0:sz], amplitude[0:sz])

    # Give a title for the wave plot
    plt.title(title)

    # Give x axis label for the wave plot
    plt.xlabel('Time')

    # Give y axis label for the wave plot
    plt.ylabel('Amplitude')
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')

    # Display the sine wave
    plt.show()


def get_fft(amplitude, rate=RATE):
    yf = rfft(amplitude)
    size = amplitude.size if isinstance(
        amplitude, np.ndarray) else len(amplitude)

    xf = rfftfreq(size, 1/rate)

    return xf, yf


def display_fft(xf, yf, title="FFT", xlim=None, ylim=None):
    if xlim is None:
        xlim = [min(xf), max(xf)]
    if ylim is None:
        ylim = [0, max(yf)]
    plt.title(f'FFT: {title}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.plot(xf, np.abs(yf))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.show()

    return xf, yf


def show_fft(amplitude, title="FFT", xlim=None, ylim=None, rate=RATE):
    xf, yf = get_fft(amplitude, rate=rate)
    display_fft(xf, yf, title=title, xlim=xlim, ylim=ylim)

    return xf, yf


def get_fft_cmplx(amplitude, rate=RATE):
    yf = fft(amplitude)
    size = amplitude.size if isinstance(
        amplitude, np.ndarray) else len(amplitude)

    xf = fftfreq(size, 1/rate)

    return xf, yf


def show_fft_cmplx(amplitude, title="FFT", xlim=None, rate=RATE):
    xf, yf = get_fft_cmplx(amplitude, rate=rate)
    if xlim is None:
        xlim = [min(xf), max(xf)]
    plt.title(f'FFT: {title}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.plot(xf, np.abs(yf))
    plt.xlim(xlim)
    plt.show()

    return xf, yf


def write_to_txt(filename, data):
    '''
        Writes wave data to .txt file that can be read by Audacity
        (Tools -> Sample Data Import...)
    '''
    with open(f'{filename.replace(".txt", "")}.txt', 'w') as f:
        for value in data:
            f.write('{:.4f} '.format(value))


if __name__ == '__main__':
    f0 = 100  # start frequency (Hz)
    f1 = 2000  # end frequency (Hz)
    a0 = 1  # start amplitude (normalised 0-1)
    a1 = 1  # end amplitude (normalised 0-1)
    clipThreshold = 1  # normalised 0-1

    CHIRP_TYPES = {
        0: 'lin',  # linear
        1: 'exp',  # exponential
        2: 'hyp',  # hyperbolic
    }
    CHOICE = 1

    time = np.arange(0, DURATION, 1/RATE)
    # amplitude = chirp(CHIRP_TYPES[CHOICE], time,
    #                   f0, f1, a0, a1, clipThreshold=clipThreshold)
    # write_to_txt('wave_gen', amplitude)

    chirp_data, inv = exp_chirp_and_inverse(time, f0, f1, a0, a1)

    plot(time, chirp_data)
    plot(time, inv)
