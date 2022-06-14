import numpy as np
from data_analysis import read_txt
from denoise import removeNoise
from scipy import signal
from scipy.fft import irfft
from wave_gen import write_to_txt, get_fft, display_fft


# def high_pass(xf, yf, cutoff, rate):
#     points_per_freq = len(xf) / (rate / 2)
#     target_idx = int(points_per_freq * cutoff)

#     filtered_yf = np.copy(yf)
#     for i in range(target_idx):
#         filtered_yf[i] = 0

#     return filtered_yf


def threshold_filter(xf, yf, threshold, scale=0):
    yf_max = max(yf)
    cutoff = yf_max * threshold

    filtered_yf = np.copy(yf)
    for i in range(filtered_yf.size):
        if filtered_yf[i] < cutoff:
            filtered_yf[i] = yf[i] * scale

    return filtered_yf


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


noise = read_txt(
    'arduino_readwrite/noise_samples/sample_19770_10s_1'
)

sig = read_txt(
    'arduino_readwrite/440_samples/sample_15700_10s_1.txt'
)


sig_xf, sig_yf = get_fft(sig, rate=17660)
display_fft(sig_xf, sig_yf, title='original', xlim=[0, 1000], ylim=[0, 200])

# sig = removeNoise(sig, noise, visual=False)

# sig_xf, sig_yf = get_fft(sig, rate=17660)
# display_fft(sig_xf, sig_yf, title='noise filtered',
#             xlim=[0, 1000], ylim=[0, 200])

sig_xf, sig_yf = butter_highpass_filter_f(sig_yf, 200, 17660)


display_fft(sig_xf, sig_yf, title='noise and low filtered', xlim=[0, 1000])

# sig_yf = threshold_filter(sig_xf, sig_yf, 0.2, scale=0.3)
# display_fft(sig_xf, sig_yf,
#             title='noise and low and threshold filtered', xlim=[0, 1000])

filtered_sig = irfft(sig_yf)

# rec = removeNoise(filtered_sig, noise, visual=False)

write_to_txt('denoised', filtered_sig)
