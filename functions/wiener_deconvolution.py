# Simple example of Wiener deconvolution in Python.
# We use a fixed SNR across all frequencies in this example.
#
# Written 2015 by Dan Stowell. Public domain.
# https://gist.github.com/danstowell/f2d81a897df9e23cc1da

import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
from functions.read_files import read_txt
from temporal_quality import temporal_quality
plt.rcParams.update({'font.size': 6})

##########################
# default values
sonlen_default = 128
irlen_default = 64

lambd_est_default = 1e-3  # estimated noise lev

##########################


def gen_son(length):
    "Generate a synthetic un-reverberated 'sound event' template"
    # (whitenoise -> integrate -> envelope -> normalise)
    son = np.cumsum(np.random.randn(length))
    # apply envelope
    attacklen = length // 8
    env = np.hstack((np.linspace(0.1, 1, attacklen),
                    np.linspace(1, 0.1, length - attacklen)))
    son *= env
    son /= np.sqrt(np.sum(son * son))
    return son


def gen_ir(length):
    "Generate a synthetic impulse response"
    # First we generate a quietish tail
    son = np.random.randn(length)
    attacklen = length // 2
    env = np.hstack((np.linspace(0.1, 1, attacklen),
                    np.linspace(1, 0.1, length - attacklen)))
    son *= env
    son *= 0.05
    # Here we add the "direct" signal
    son[0] = 1
    # Now some early reflection spikes
    for _ in range(10):
        son[int(length * (np.random.rand()**2))] += np.random.randn() * 0.5
    # Normalise and return
    son /= np.sqrt(np.sum(son * son))
    return son


def wiener_deconvolution(signal, kernel, lambd, snip=False):
    "lambd is the SNR"
    # zero pad the kernel to same length
    kernel = np.hstack((kernel, np.zeros(len(signal) - len(kernel))))
    H = fft(kernel)
    deconvolved = np.real(ifft(
        fft(signal) * np.conj(H) /
        # TODO shouldn't it be (H*np.conj(H)*fft(signal) + lambd**2) ??
        (H*np.conj(H) + lambd**2)
    ))
    if snip:
        deconvolved = deconvolved[1*deconvolved.size//3:2*deconvolved.size//3]
    return deconvolved


def test_wiener(obs, ir, lambd=lambd_est_default, snip=False):
    son_est = wiener_deconvolution(
        obs, ir,  lambd=lambd, snip=snip)
    obs_est = np.convolve(son_est, ir, mode='full')

    # plot
    plt.figure(frameon=False)

    plt.subplot(3, 2, 3)
    plt.plot(son_est)
    plt.title("son_est")
    plt.subplot(3, 2, 2)
    plt.plot(ir)
    plt.title("ir")
    plt.subplot(3, 2, 4)
    plt.plot(obs_est)
    plt.title("obs_est")
    plt.subplot(3, 1, 3)
    plt.plot(obs)
    plt.title("obs")
    #
    plt.tight_layout()
    plt.show()
    #
    plt.close()

    return son_est


def get_wiener(obs, ir, lambd, snip=False):
    son_est = wiener_deconvolution(
        obs, ir,  lambd=lambd, snip=snip)
    obs_est = np.convolve(son_est, ir, mode='full')

    return obs_est


def get_wiener_error(obs, obs_est):
    obs_len = len(obs)

    if len(obs_est) != obs_len:
        print(obs_len, len(obs_est))
        return print('length not the same')

    return np.sqrt(np.mean((obs - obs_est) ** 2))


def compare_wiener_snr(obs, ir, lambdas, logMode='plot'):
    """
    compares different lambda (SNR) values and see which produces the best estimate
    """
    wieners = []
    # obs_sz = len(obs)
    for lm in lambdas:
        obs_est = get_wiener(obs, ir, lm, snip=False)
        wieners.append(obs_est)

    num_plots = len(lambdas)

    if logMode == 'plot':
        # plot
        plt.figure(frameon=False)

        plt.subplot(num_plots+1, 1, 1)
        plt.plot(obs)
        plt.title('Unit Impulse')

    for i, est in enumerate(wieners):
        peak, tq = temporal_quality(est)

        if logMode == 'plot':
            plt.subplot(num_plots+1, 1, i+2)
            plt.plot(est)
            plt.title(
                f'Wiener estimate with λ={lambdas[i]}, Temporal quality={tq}')
        elif logMode == 'print':
            print(f'Wiener estimate with λ={lambdas[i]}, Temporal quality={tq}')

    if logMode == 'plot':
        #
        plt.tight_layout()
        plt.show()
        #
        plt.close()


def wiener_estimate_snr(ir, lambdas, verbose=False):
    """
    given an array of lambdas, assuming a singular maximum peak,
    find the lambda (SNR) that produces the best temporal quality
    when unit impulse is deconvolved by given impulse response \n
    returns the deconvolution result h'(t)
    """
    def print_result(lm, tq=None):
        if tq is None:
            est = get_wiener(delta, ir, lm, snip=False)
            _, tq = temporal_quality(est)

        print('===')
        print(f'The best Lambda is {lm}, which yields tq={tq}')
        print('===')
        print()

    delta = np.zeros(ir.size)
    delta[0] = 1

    if len(lambdas) == 1:
        print_result(lambdas[0])
        return lambdas[0]

    if len(lambdas) == 2:
        left_est = get_wiener(delta, ir, delta[0], snip=False)
        right_est = get_wiener(delta, ir, delta[1], snip=False)

        _, left_tq = temporal_quality(left_est)
        _, right_tq = temporal_quality(right_est)

        result = lambdas[0] if left_tq > right_tq else lambdas[1]
        print_result(result)

        return result

    seg = lambdas

    while len(seg) > 0:
        ptr = len(seg)//2

        left_seg = seg[0:ptr]
        right_seg = seg[ptr+1:len(seg)]

        if len(left_seg) == 0 or len(right_seg) == 0:
            result = seg[ptr]
            print_result(result)
            return result

        left_est = get_wiener(delta, ir, seg[ptr-1], snip=False)
        mid_est = get_wiener(delta, ir, seg[ptr], snip=False)
        right_est = get_wiener(delta, ir, seg[ptr+1], snip=False)
        _, left_tq = temporal_quality(left_est)
        _, mid_tq = temporal_quality(mid_est)
        _, right_tq = temporal_quality(right_est)

        max_tq = max(left_tq, mid_tq, right_tq)
        if max_tq == mid_tq:
            verbose and print('max is mid', left_tq, mid_tq, right_tq)
            result = seg[ptr]
            print_result(result, mid_tq)
            return result

        elif max_tq == left_tq:
            verbose and print('max is left', left_tq, mid_tq, right_tq)
            seg = left_seg
        else:
            verbose and print('max is right', left_tq, mid_tq, right_tq)
            seg = right_seg

        verbose and print(f'Search length remaining: {len(seg)}')


if __name__ == '__main__':
    sig_h = read_txt('../signal_data/response/rt1.Wfm_denoised_xcorr.txt')
    lambdas = np.linspace(0, 5, 101)
    wiener_estimate_snr(sig_h, lambdas, verbose=True)
