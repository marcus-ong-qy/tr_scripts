# -*- coding: utf-8 -*-
"""
Inverse Filter of a freaking chirp
https://dsp.stackexchange.com/questions/41696/calculating-the-inverse-filter-for-the-exponential-sine-sweep-method/41700#41700
"""

from __future__ import division
import numpy as np

from scipy import signal
from config import RATE, DURATION
from wave_gen import plot, write_to_txt, norm, show_fft, reverse, \
    exp_chirp_and_inverse, timeline
from data_analysis import read_txt
from oscilloscope_read_csv_to_txt import _process_suffix


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


def xcorr_old(
        chirp, sig_path, output_path=None, showPlot=False):

    # chirp_path = _process_suffix(chirp_path, '.txt')
    sig_path = _process_suffix(sig_path, '.txt')

    if output_path is None:
        output_path = f'{sig_path[:-4]}_xcorr_old.txt'

    # emitted signal s(t)
    sig_s = chirp  # read_txt(chirp_path)

    # detected signal r(t)
    sig_r = read_txt(sig_path)

    # Cross-correlation h(t)
    sig_h = signal.correlate(sig_r, sig_s)

    # sig_y = signal.convolve(sig_h[::-1], sig_h)

    if showPlot:
        plot(timeline(sig_s), sig_s, sample_sz=-
             1, title='xcorr_trad sig_s s(t)')

        plot(timeline(sig_r), sig_r, sample_sz=-
             1, title='xcorr_trad sig_r r(t)')
        show_fft(sig_r, title="xcorr_trad sig_r")

        plot(timeline(sig_h),
             sig_h, sample_sz=-1, title='xcorr_trad sig_h h(t)')
        # show_fft(sig_h, title="sig_h")

        sig_y = norm(signal.correlate(sig_h, sig_h))

        plot(timeline(sig_y),
             sig_y, sample_sz=-1, title='xcorr_trad sig_y y(t)')

    data = reverse(norm(sig_h))

    write_to_txt(output_path, data)


# It is more better because I use inv_chirp_data to convolve
def xcorr(
        chirp_data, inv_chirp_data, sig_path,
        output_path=None, showPlot=False):

    sig_path = _process_suffix(sig_path, '.txt')

    if output_path is None:
        output_path = f'{sig_path[:-4]}_xcorr.txt'

    # emitted signal s(t)
    sig_s, inv_sig_s = chirp_data, inv_chirp_data

    # detected signal r(t)
    sig_r = read_txt(sig_path)

    # Convolution h(t)
    sig_h = signal.convolve(sig_r, inv_sig_s)

    if showPlot:
        plot(timeline(sig_s), sig_s, sample_sz=-1,
             title='xcorr_more_better sig_s s(t)')
        plot(timeline(inv_sig_s), inv_sig_s, sample_sz=-
             1, title='xcorr_more_better inverse filter of s(t)')

        plot(timeline(sig_r), sig_r, sample_sz=-1,
             title='xcorr_more_better sig_r r(t)')
        show_fft(sig_r, title="xcorr_more_better sig_r")

        plot(timeline(sig_h),
             sig_h, sample_sz=-1, title='xcorr_more_better sig_h h(t)')
        # show_fft(sig_h, title="sig_h")

        sig_y = norm(signal.correlate(sig_h, sig_h))

        plot(timeline(sig_y),
             sig_y, sample_sz=-1, title='xcorr_more_better sig_y y(t)')

    data = reverse(norm(sig_h))

    write_to_txt(output_path, data)


if __name__ == "__main__":
    f0 = 100  # start frequency (Hz)
    f1 = 2000  # end frequency (Hz)
    a0 = 1  # start amplitude (normalised 0-1)
    a1 = 1  # end amplitude (normalised 0-1)
    clipThreshold = 1  # normalised 0-1

    time = np.arange(0, DURATION, 1/RATE)

    chirp_data, inv = exp_chirp_and_inverse(time, f0, f1, a0, a1)

    READ_PATH = 'oscilloscope/chirp/chirp1.Wfm_denoised.txt'

    xcorr_more_better(
        chirp_data, inv, READ_PATH, showPlot=True)

    # plot(time, chirp_data)
    # plot(time, inv)

    # plt.show()
