# Simple example of Wiener deconvolution in Python.
# We use a fixed SNR across all frequencies in this example.
#
# Written 2015 by Dan Stowell. Public domain.
# https://gist.github.com/danstowell/f2d81a897df9e23cc1da

import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
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
        obs, ir,  lambd=lambd, snip=snip)  # [:sonlen_default]
    obs_est = np.convolve(son_est, ir, mode='full')  # [:obslen]

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
        obs, ir,  lambd=lambd, snip=snip)  # [:sonlen_default]
    # ir_est  = wiener_deconvolution(obs, son, lambd=lambd_est_default)[:irlen_default]
    obs_est = np.convolve(son_est, ir, mode='full')  # [:obslen]

    return obs_est


def get_wiener_error(obs, obs_est):
    obs_len = len(obs)

    if len(obs_est) != obs_len:
        print(obs_len, len(obs_est))
        return print('length don\'t same')

    return np.sqrt(np.mean((obs - obs_est) ** 2))


def compare_wieners(obs, ir, lambdas, logMode='plot'):
    """
    compares different lambda (SNR) values and see which produces the largest
    wiener
    """
    wieners = []
    # obs_sz = len(obs)
    for lm in lambdas:
        obs_est = get_wiener(obs, ir, lm, snip=False)
        wieners.append(obs_est  # [len(obs_est)-obs_sz+1:]
                       )

    num_plots = len(lambdas)

    if logMode == 'plot':
        # plot
        plt.figure(frameon=False)

        plt.subplot(num_plots+1, 1, 1)
        plt.plot(obs)
        plt.title('OG Wiener')

    for i, est in enumerate(wieners):
        peak, tq = temporal_quality(est)

        if logMode == 'plot':
            plt.subplot(num_plots+1, 1, i+2)
            plt.plot(est)
            plt.title(
                f'Wiener with λ={lambdas[i]}, Temporal quality={tq}')
        elif logMode == 'print':
            print(f'Wiener with λ={lambdas[i]}, Temporal quality={tq}')

    if logMode == 'plot':
        #
        plt.tight_layout()
        plt.show()
        #
        plt.close()


def get_best_wiener(ir, lambdas, verbose=False):
    """
    given an array of lambdas, assuming a singular maximum peak,
    find the lambda that produces the best temporal quality
    when unit impulse is deconvolved by given impulse response

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


def sample():
    """
    simple test: get one soundtype and one impulse response, convolve them,
    deconvolve them, and check the result (plot it!)
    """
    son = gen_son(sonlen_default)
    ir = gen_ir(irlen_default)
    obs = np.convolve(son, ir, mode='full')
    # let's add some noise to the obs
    obs += np.random.randn(*obs.shape) * lambd_est_default
    son_est = wiener_deconvolution(obs, ir,  lambd=lambd_est_default)[:sonlen_default]
    ir_est = wiener_deconvolution(obs, son, lambd=lambd_est_default)[:irlen_default]
    # calc error
    son_err = np.sqrt(np.mean((son - son_est) ** 2))
    ir_err = np.sqrt(np.mean((ir - ir_est) ** 2))
    print(
        "single_example_test(): RMS errors son %g, IR %g" % (son_err, ir_err))

    # plot
    plt.figure(frameon=False)
    #
    plt.subplot(3, 2, 1)
    plt.plot(son)
    plt.title("son")
    plt.subplot(3, 2, 3)
    plt.plot(son_est)
    plt.title("son_est")
    plt.subplot(3, 2, 2)
    plt.plot(ir)
    plt.title("ir")
    plt.subplot(3, 2, 4)
    plt.plot(ir_est)
    plt.title("ir_est")
    plt.subplot(3, 1, 3)
    plt.plot(obs)
    plt.title("obs")
    #
    plt.tight_layout()
    plt.show()
    #
    plt.close()


if __name__ == '__main__':
    sample()
