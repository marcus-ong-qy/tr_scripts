import librosa
from librosa import display
import sklearn as sk
import matplotlib.pyplot as plt
# from playsound import playsound # if playsound fails to install on mac, try 'pip install pyobjc' first
import numpy as np
import sys
from scipy import signal

def read_txt(filename):
    with open(f'{filename.replace(".txt", "")}.txt', 'r') as f:
        data_arr = f.read().split()
        data = np.array(list(map(float, list(data_arr))))

    return data

def spectrogram(y, xlimit=None):
    # y, sr = librosa.load(file_name)
    y = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    # plt.title(file_name)
    librosa.display.specshow(y, x_axis='time', y_axis='linear');
    plt.colorbar();
    if xlimit:
        plt.xlim(0, xlimit)
    plt.show()

def next_pow2(x):
    if x == 0:
        return 1
    else:
        n = 2;
        while n < x:
            n = n*2
        return n

def deconv(y, x, ir = True):
    # y, sry = librosa.load(combined_filename)
    # x, srx = librosa.load(audioir_filename) # used var name x, but can be x or h (original audio or impulse response)

    scale = 4

    N = next_pow2(y.shape[0])   
    ft_y = np.fft.rfft(y, N)
    ft_x = np.fft.rfft(x, N)

    recovered = np.fft.irfft(ft_y * np.conj(ft_x)/(abs(ft_x)**2))

    recovered = recovered * scale

    return recovered
    
    # if ir:
    #     # librosa.output.write_wav("recovered_ir.wav", recovered, srx)
    #     return "recovered_ir.wav"
    # else:
    #     # librosa.output.write_wav("recovered_audio.wav", recovered, srx)
    #     return "recovered_audio.wav"

def conv(audio_filename, ir_filename):
    x, srx = librosa.load(audio_filename) # original audio
    h, srh = librosa.load(ir_filename) # impulse response

    if srx != srh:
        sys.exit('sr must be the same in both files')

    N = next_pow2(max(x.shape[0],h.shape[0]))
    scale = 0.3

    y = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(h, N))
    y *= scale
    
    # librosa.output.write_wav("combined.wav", y, srx)
    return "combined.wav", y.shape[0] - x.shape[0]



RATE = 25000  # sampling rate in Hz
DURATION = 0.5  # duration of signal, in seconds
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

def timeline(amplitude):
    time = np.arange(0, DURATION, 1/RATE)
    return np.arange(0, DURATION*(len(amplitude)/time.size), 1/RATE)

if __name__ == '__main__':
    sig_path = 'oscilloscope/chirp/chirp1.Wfm.txt'
    chirp_path = 'oscilloscope/chirp/chirp_exp_100-2000_1-1_clip1'

    # emitted signal s(t)
    sig_s = read_txt(chirp_path)

    # detected signal r(t)
    sig_r = read_txt(sig_path)

    # Cross-correlation h(t)
    sig_h = signal.correlate(sig_r, sig_s)

    impulse_signal = np.zeros(sig_h.size)
    impulse_signal[0] = 1

    sig_h_decon = deconv(impulse_signal, sig_h)
    plot(timeline(sig_s), sig_s, sample_sz=-1, title='sig_s s(t)')

    plot(timeline(sig_r), sig_r, sample_sz=-1, title='sig_r r(t)')

    plot(timeline(sig_h),
            sig_h, sample_sz=-1, title='sig_h h(t)')

    plot(timeline(sig_h_decon),
            sig_h_decon, sample_sz=-1, title='sig_h_decon h(t)')

    impulse_recon = np.convolve(sig_h_decon, sig_h)

    plot(timeline(impulse_recon),
            impulse_recon, sample_sz=-1, title='impulse_recon')

# impulse_response = "Philips_mono.wav"#"Concertgebouw-m.wav"
# audio_file = 'anechoic1.wav'#"Beethoven_Symph7.wav"
# combined, diff = conv(audio_file, impulse_response)
# re_ir = deconv(combined, audio_file)
# re_aud = deconv(combined, impulse_response, ir = False)

# spectrogram(sig_h)

# spectrogram(impulse_signal)

# spectrogram(sig_h_decon)

# ir = librosa.load(impulse_response) # scale the spectrogram to the length of the original impulse response, this helps with comparison
# ir_length = ir[0].shape[0]/ir[1]
# spectrogram(re_ir, xlimit=ir_length)

# aud = librosa.load(audio_file) # scale the spectrogram to the length of the original audio, this helps with comparison
# aud_length = aud[0].shape[0]/aud[1]
# spectrogram(re_aud, xlimit = aud_length)