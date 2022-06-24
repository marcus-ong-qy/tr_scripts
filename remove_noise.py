import numpy as np
from config import RATE
from data_analysis import read_txt
from denoise import removeNoise
from scipy import signal
from scipy.fft import irfft
from wave_gen import write_to_txt, get_fft, display_fft
from oscilloscope_read_csv_to_txt import _process_suffix


def threshold_filter(xf, yf, threshold, scale=0):
    yf_max = max(yf)
    cutoff = yf_max * threshold

    filtered_yf = np.copy(yf)
    for i in range(filtered_yf.size):
        if filtered_yf[i] < cutoff:
            filtered_yf[i] = yf[i] * scale

    return filtered_yf

# TODO zero function


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype="high", analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def butter_highpass_filter_f(data, cutoff, fs, order=5):
    '''
    butter highpass that takes in Fourier data instead
    '''
    sig = irfft(data)
    y = butter_highpass_filter(sig, cutoff, fs, order=order)
    xf, yf = get_fft(y, rate=fs)
    return xf, yf


NOISE_PATH = 'oscilloscope/noisesamp/sensornoise1.Wfm.txt'
SIG_PATH = 'oscilloscope/chirp/chirp1.Wfm'


def remove_noise(sig_path, noise_path, plot=True, xlim=None, ylim=None):
    noise_path = _process_suffix(noise_path, '.txt')
    sig_path = _process_suffix(sig_path, '.txt')

    noise = read_txt(noise_path)
    sig = read_txt(sig_path)

    sig_xf, sig_yf = get_fft(sig)

    plot and display_fft(sig_xf, sig_yf, title='original',
                         xlim=xlim, ylim=ylim)

    sig = removeNoise(sig, noise, visual=False)
    sig_xf, sig_yf = get_fft(sig)

    plot and display_fft(
        sig_xf, sig_yf, title='noise filtered', xlim=xlim, ylim=ylim)

    sig_xf, sig_yf = butter_highpass_filter_f(sig_yf, 200, RATE)

    plot and display_fft(
        sig_xf, sig_yf, title='noise and low filtered', xlim=xlim, ylim=ylim)

    # sig_yf = threshold_filter(sig_xf, sig_yf, 0.2, scale=0.3)
    # display_fft(sig_xf, sig_yf,
    #             title='noise and low and threshold filtered', xlim=[0, 1000])

    filtered_sig = irfft(sig_yf)

    # rec = removeNoise(filtered_sig, noise, visual=False)

    denoised_txt_file = f'{sig_path[:-4]}_denoised.txt'
    write_to_txt(denoised_txt_file, filtered_sig)

    return denoised_txt_file


if __name__ == '__main__':
    remove_noise(SIG_PATH, NOISE_PATH, xlim=[0, 1000], ylim=[0, 200])
