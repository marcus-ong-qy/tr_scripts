# Simple example of Wiener deconvolution in Python.
# We use a fixed SNR across all frequencies in this example.
#
# Written 2015 by Dan Stowell. Public domain.
# https://gist.github.com/danstowell/f2d81a897df9e23cc1da

import numpy as np
from numpy.fft import fft, ifft, ifftshift

import matplotlib
# matplotlib.use('PDF') # http://www.astrobetter.com/plotting-to-a-file-in-python/
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'font.size': 6})

##########################
# user config
sonlen = 128
irlen = 64

lambd_est = 1e-3  # estimated noise lev

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


def test_wiener(obs, ir, lambd=lambd_est, snip=False):
    son_est = wiener_deconvolution(
        obs, ir,  lambd=lambd, snip=snip)  # [:sonlen]
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
        obs, ir,  lambd=lambd, snip=snip)  # [:sonlen]
    # ir_est  = wiener_deconvolution(obs, son, lambd=lambd_est)[:irlen]
    obs_est = np.convolve(son_est, ir, mode='full')  # [:obslen]

    return obs_est


def get_wiener_error(obs, obs_est):
    obs_len = len(obs)

    if len(obs_est) != obs_len:
        print(obs_len, len(obs_est))
        return print('length don\'t same')

    return np.sqrt(np.mean((obs - obs_est) ** 2))


def compare_wieners(obs, ir, lambdas):
    """
    compares different lambda (SNR) values and see which produces the largest wiener

    """
    wieners = []
    obs_sz = len(obs)
    for l in lambdas:
        obs_est = get_wiener(obs, ir, l, snip=False)
        wieners.append(obs_est[len(obs_est)-obs_sz+1:])

    num_plots = len(lambdas)

    # plot
    plt.figure(frameon=False)

    plt.subplot(num_plots+1, 1, 1)
    plt.plot(obs)
    plt.title('OG Wiener')

    for i, est in enumerate(wieners):
        # TODO perhaps use temporal_quality?
        error = get_wiener_error(obs[:-1], est)
        plt.subplot(num_plots+1, 1, i+2)
        plt.plot(est)
        plt.title(f'Wiener with λ={lambdas[i]}, error={error}')
    #
    plt.tight_layout()
    plt.show()
    #
    plt.close()


def sample():
    "simple test: get one soundtype and one impulse response, convolve them, deconvolve them, and check the result (plot it!)"
    son = gen_son(sonlen)
    ir = gen_ir(irlen)
    obs = np.convolve(son, ir, mode='full')
    # let's add some noise to the obs
    obs += np.random.randn(*obs.shape) * lambd_est
    son_est = wiener_deconvolution(obs, ir,  lambd=lambd_est)[:sonlen]
    ir_est = wiener_deconvolution(obs, son, lambd=lambd_est)[:irlen]
    # calc error
    son_err = np.sqrt(np.mean((son - son_est) ** 2))
    ir_err = np.sqrt(np.mean((ir - ir_est) ** 2))
    print("single_example_test(): RMS errors son %g, IR %g" % (son_err, ir_err))
    # plot
    pdf = PdfPages('wiener_deconvolution_example.pdf')
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
    pdf.savefig()
    plt.close()
    pdf.close()


if __name__ == '__main__':
    sample()
