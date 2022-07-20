# -*- coding: utf-8 -*-
"""
Inverse Filter of a freaking chirp
https://dsp.stackexchange.com/questions/41696/calculating-the-inverse-filter-for-the-exponential-sine-sweep-method/41700#41700
"""

from __future__ import division
import numpy as np
from scipy import signal

from config import RATE, DURATION
from functions.wave_gen import plot, write_to_txt, norm, show_fft, reverse, \
    exp_chirp_and_inverse, timeline
from functions.read_files import read_osc_csv


def dbfft(x, fs, win=None):
    N = len(x)  # Length of input sequence

    if win is None:
        win = np.ones(x.shape)
    if len(x) != len(win):
        raise ValueError('Signal and window must be of the same length')
    x = x * win

    # Calculate real FFT and frequency vector
    sp = np.fft.rfft(x)
    freq = np.arange((N / 2) + 1) / (float(N) / fs)

    # Scale the magnitude of FFT by window and factor of 2,
    # because we are using half of FFT spectrum.
    s_mag = np.abs(sp) * 2 / np.sum(win)

    # Convert to dBFS
    ref = s_mag.max()
    s_dbfs = 20 * np.log10(s_mag/ref)

    return freq, s_dbfs


# It is more better because I use inv_chirp_data to convolve
def xcorr(chirp_data, inv_chirp_data, sig_r,
          output_path=None, showPlot=False):

    # emitted signal s(t)
    sig_s, inv_sig_s = chirp_data, inv_chirp_data

    # Convolution h(t)
    sig_h = signal.convolve(sig_r, inv_sig_s)

    if showPlot:
        plot(timeline(sig_s), sig_s, sample_sz=-1,
             title='xcorr sig_s s(t)')
        plot(timeline(inv_sig_s), inv_sig_s, sample_sz=-
             1, title='xcorr_more_better inverse filter of s(t)')

        plot(timeline(sig_r), sig_r, sample_sz=-1,
             title='xcorr sig_r r(t)')
        show_fft(sig_r, title="xcorr sig_r")

        plot(timeline(sig_h),
             sig_h, sample_sz=-1, title='xcorr sig_h h(t)')
        show_fft(sig_h, title="sig_h")

        sig_y = norm(signal.correlate(sig_h, sig_h))

        plot(timeline(sig_y),
             sig_y, sample_sz=-1, title='xcorr sig_y y(t)')

    data = reverse(norm(sig_h))
    if output_path:
        write_to_txt(output_path, data)

    return data


if __name__ == "__main__":
    f0 = 100  # start frequency (Hz)
    f1 = 2000  # end frequency (Hz)
    a0 = 1  # start amplitude (normalised 0-1)
    a1 = 1  # end amplitude (normalised 0-1)
    clipThreshold = 1  # normalised 0-1

    time = np.arange(0, DURATION, 1/RATE)

    chirp_data, inv = exp_chirp_and_inverse(time, f0, f1, a0, a1)

    READ_PATH = 'signal_data/response/rt1.Wfm'

    sig_r = read_osc_csv(READ_PATH)

    xcorr(chirp_data, inv, READ_PATH, showPlot=True)
