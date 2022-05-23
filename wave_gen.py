# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:53:42 2022

@author: OQinYuan
"""

import numpy as np


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


def chirp(waveFn, time, f0, f1, a0, a1, waveType="sine"):
    """
        waveFn: 'lin' (default), 'exp', 'hyp' \n
        time: array of time axis values \n
        f0: start frequency (Hz) \n
        f1: end frequency (Hz) \n
        a0: start amplitude (normalised 0-1) \n
        a1: end amplitude (normalised 0-1)
        waveType: 'sine' (default), 'square'
    """
    if waveFn == 'exp':
        wave = exp_chirp(time, f0, f1, a0, a1)
    elif waveFn == 'hyp':
        wave = hyp_chirp(time, f0, f1, a0, a1)
    else:
        wave = lin_chirp(time, f0, f1, a0, a1)

    return square(wave) if waveType == 'square' else wave


def rand_noise():
    import random
    amplitude = []
    for _ in range(RATE*DURATION):
        amplitude.append(2*random.random() - 1)
    return amplitude


def write_to_txt(filename, data):
    '''
        Writes wave data to .txt file that can be read by Audacity
        (Tools -> Sample Data Import...)
    '''
    with open(f'{filename.replace(".txt", "")}.txt', 'w') as f:
        for value in data:
            f.write('{:.4f} '.format(value))


RATE = 44100  # sampling rate in Hz
DURATION = 0.5  # duration of signal, in seconds

f0 = 100  # start frequency (Hz)
f1 = 2000  # end frequency (Hz)
a0 = 1  # start amplitude (normalised 0-1)
a1 = 1  # end amplitude (normalised 0-1)

CHIRP_TYPES = {
    0: 'lin',  # linear
    1: 'exp',  # exponential
    2: 'hyp',  # hyperbolic
}
CHOICE = 1

if __name__ == '__main__':
    time = np.arange(0, DURATION, 1/RATE)
    amplitude = chirp(CHIRP_TYPES[CHOICE], time,
                      f0, f1, a0, a1, waveType='square')
    write_to_txt('wave_gen', amplitude)

# # Plot
# import matplotlib.pyplot as plot
# # Plot a sine wave using time and amplitude obtained for the sine wave
# plot.plot(time, amplitude)

# # Give a title for the sine wave plot
# plot.title('Sine wave')

# # Give x axis label for the sine wave plot
# plot.xlabel('Time')

# # Give y axis label for the sine wave plot
# plot.ylabel('Amplitude = sin(time)')
# plot.grid(True, which='both')
# plot.axhline(y=0, color='k')
# plot.show()

# # Display the sine wave
# plot.show()
