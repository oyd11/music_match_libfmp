

import logging

import numpy as np
import librosa
from scipy import ndimage
from matplotlib import pyplot as plt

import libfmp.b


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)


def compute_constellation_map(Y, dist_freq=7, dist_time=7, thresh=0.01):
    """Compute constellation map (implementation using image processing)

    Notebook: C7/C7S1_AudioIdentification.ipynb

    Args:
        Y (np.ndarray): Spectrogram (magnitude)
        dist_freq (int): Neighborhood parameter for frequency direction (kappa) (Default value = 7)
        dist_time (int): Neighborhood parameter for time direction (tau) (Default value = 7)
        thresh (float): Threshold parameter for minimal peak magnitude (Default value = 0.01)

    Returns:
        Cmap (np.ndarray): Boolean mask for peak structure (same size as Y)
    """
    result = ndimage.maximum_filter(
        Y, size=[2 * dist_freq + 1, 2 * dist_time + 1],
        mode='constant')
    Cmap = np.logical_and(Y == result, result > thresh)
    return Cmap


def compute_spectrogram(fn, Fs=22050,
                        duration=None,
                        N=2048, H=1024,
                        bin_max=128, frame_max=None):
    x, Fs = librosa.load(fn, sr=Fs, duration=duration, mono=True)
    x_duration = len(x) / Fs  # noqa
    X = librosa.stft(x, n_fft=N, hop_length=H, win_length=N, window='hann')
    if bin_max is None:
        bin_max = X.shape[0]
    if frame_max is None:
        frame_max = X.shape[1]
    Y = np.abs(X[:bin_max, :frame_max])
    return Y, x_duration


def match_binary_matrices_tol(C_ref, C_est, tol_freq=0, tol_time=0):
    """| Compare binary matrices with tolerance
    | Note: The tolerance parameters should be smaller than the minimum distance of
      peaks (1-entries in C_ref ad C_est) to obtain meaningful TP, FN, FP values

    Notebook: C7/C7S1_AudioIdentification.ipynb

    Args:
        C_ref (np.ndarray): Binary matrix used as reference
        C_est (np.ndarray): Binary matrix used as estimation
        tol_freq (int): Tolerance in frequency direction (vertical) (Default value = 0)
        tol_time (int): Tolerance in time direction (horizontal) (Default value = 0)

    Returns:
        TP (int): True positives
        FN (int): False negatives
        FP (int): False positives
        C_AND (np.ndarray): Boolean mask of AND of C_ref and C_est (with tolerance)
    """
    assert C_ref.shape == C_est.shape, "Dimensions need to agree"
    N = np.sum(C_ref)
    M = np.sum(C_est)
    # Expand C_est with 2D-max-filter using the tolerance parameters
    C_est_max = ndimage.maximum_filter(
        C_est, size=(2 * tol_freq + 1, 2 * tol_time + 1),
        mode='constant')
    C_AND = np.logical_and(C_est_max, C_ref)
    TP = np.sum(C_AND)
    FN = N - TP
    FP = M - TP
    return TP, FN, FP, C_AND


def compute_matching_function(C_D, C_Q, tol_freq=1, tol_time=1):
    """Computes matching function for constellation maps

    Notebook: C7/C7S1_AudioIdentification.ipynb

    Args:
        C_D (np.ndarray): Binary matrix used as dababase document
        C_Q (np.ndarray): Binary matrix used as query document
        tol_freq (int): Tolerance in frequency direction (vertical) (Default value = 1)
        tol_time (int): Tolerance in time direction (horizontal) (Default value = 1)

    Returns:
        Delta (np.ndarray): Matching function
        shift_max (int): Optimal shift position maximizing Delta
    """
    L = C_D.shape[1]
    N = C_Q.shape[1]
    M = L - N + 1
    assert M >= 0, "Query must be shorter than document"
    Delta = np.zeros(M)
    for m in range(M):
        C_D_crop = C_D[:, m:m+N]
        TP, FN, FP, C_AND = match_binary_matrices_tol(
            C_D_crop, C_Q, tol_freq=tol_freq, tol_time=tol_time)
        Delta[m] = int(TP)
    shift_max = int(np.argmax(Delta))
    return Delta, shift_max


def tst(fn_D):
    dist_freq = 11
    dist_time = 5

    def match_with_D(fn_Q):
        logger.info(f'match_with_D called! {fn_D=} {fn_Q=}')
        Y_D, t_D = compute_spectrogram(fn_D, duration=None)
        Y_Q, t_Q = compute_spectrogram(fn_Q, duration=None)
        logger.info(
            f'Match dims: D: {Y_D.size}, {t_D}sec; {Y_Q.size}, {t_Q}sec ')
        Cmap_D = compute_constellation_map(Y_D, dist_freq, dist_time)
        Cmap_Q = compute_constellation_map(Y_Q, dist_freq, dist_time)

        Delta_0, shift_max_0 = compute_matching_function(Cmap_D, Cmap_Q, tol_freq=0, tol_time=0)
        Delta_1, shift_max_1 = compute_matching_function(Cmap_D, Cmap_Q, tol_freq=1, tol_time=1)
        Delta_2, shift_max_2 = compute_matching_function(Cmap_D, Cmap_Q, tol_freq=3, tol_time=2)

        y_max = Delta_2[shift_max_2] + 1
        fig, ax, line = libfmp.b.plot_signal(Delta_0, ylim=[0, y_max], color='g',
                                            xlabel='Shift (samples)', ylabel='Number of matching peaks',
                                            figsize=(7, 3))
        plt.title('Matching functions for different tolerance parameters')
        ax.plot(Delta_1, color='r')
        ax.plot(Delta_2, color='b')
        plt.legend(['tol_freq=0, tol_time=0', 'tol_freq=1, tol_time=1',
                    'tol_freq=3, tol_time=2'], loc='upper right', framealpha=1)
        # plt.show()
        plt.savefig('match.png')

        offset = int(shift_max_1)
        delta = int(Delta_1[offset])

        return delta, offset

    return match_with_D
