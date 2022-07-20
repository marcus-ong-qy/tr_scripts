import numpy as np
from scipy import signal
from scipy.fft import irfft

from config import RATE
from functions.wave_gen import write_to_txt, get_fft, display_fft
from functions.denoise import removeNoise
from functions.read_files import read_osc_csv,  read_txt


def threshold_filter(yf, threshold, scale=0):
    yf_max = max(yf)
    cutoff = yf_max * threshold

    filtered_yf = np.copy(yf)
    for i in range(filtered_yf.size):
        if filtered_yf[i] < cutoff:
            filtered_yf[i] = yf[i] * scale

    return filtered_yf


def _butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype="high", analog=False)
    return b, a


def _butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = _butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def butter_highpass_filter_f(data, cutoff, fs=RATE, order=5):
    '''
    butter highpass that takes in Fourier data instead
    '''
    sig = irfft(data)
    y = _butter_highpass_filter(sig, cutoff, fs, order=order)
    xf, yf = get_fft(y, rate=fs)
    return xf, yf


def _remove_noise_txt(sig_path, noise_path, highpassCutoff=None, write=True,
                      plot=True, xlim=None, ylim=None):
    """shouldn't be used"""
    writeToPath = f'{sig_path[:-4]}_denoised.txt' if write else None
    sig = read_txt(sig_path)
    noise = read_txt(noise_path)
    return remove_noise(sig, noise, highpassCutoff=highpassCutoff,
                        writeToPath=writeToPath,
                        plot=plot, xlim=xlim, ylim=ylim)


def remove_noise_csv(sig_path, noise_path, highpassCutoff=None, write=True,
                     plot=True, xlim=None, ylim=None):
    writeToPath = f'{sig_path[:-4]}_denoised.txt' if write else None
    sig = read_osc_csv(sig_path)
    noise = read_osc_csv(noise_path)
    return remove_noise(sig, noise, highpassCutoff=highpassCutoff,
                        writeToPath=writeToPath,
                        plot=plot, xlim=xlim, ylim=ylim)


def remove_noise(sig, noise, highpassCutoff=None, writeToPath=None,
                 plot=True, xlim=None, ylim=None):
    """
    removes noise from sig sample, given noise sample\n
    """

    sig_xf, sig_yf = get_fft(sig)

    plot and display_fft(sig_xf, sig_yf, title='original',
                         xlim=xlim, ylim=ylim)

    sig = removeNoise(sig, noise, visual=False)
    sig_xf, sig_yf = get_fft(sig)

    plot and display_fft(
        sig_xf, sig_yf, title='noise filtered', xlim=xlim, ylim=ylim)

    if highpassCutoff is not None:
        sig_xf, sig_yf = butter_highpass_filter_f(sig_yf, highpassCutoff)

        plot and display_fft(
            sig_xf, sig_yf, title='noise and low filtered',
            xlim=xlim, ylim=ylim)

    # sig_yf = threshold_filter(sig_yf, 0.2, scale=0.3)
    # display_fft(sig_xf, sig_yf,
    #             title='noise and low and threshold filtered', xlim=[0, 1000])

    filtered_sig = irfft(sig_yf)

    # rec = removeNoise(filtered_sig, noise, visual=False)

    if writeToPath:
        denoised_txt_file = writeToPath
        write_to_txt(denoised_txt_file, filtered_sig)

    return filtered_sig


if __name__ == '__main__':
    NOISE_PATH = 'oscilloscope/noisesamp/sensornoise1.Wfm'
    SIG_PATH = 'oscilloscope/chirp/chirp1.Wfm'

    remove_noise_csv(SIG_PATH, NOISE_PATH, highpassCutoff=200,
                     xlim=[0, 200], ylim=[0, 200])
