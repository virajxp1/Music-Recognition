import time
from scipy import signal
from scipy.signal.signaltools import wiener
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from skimage.restoration import denoise_wavelet


def audioFilter(audio,samplingrate):
    filtered_audio = wiener(audio)  # Filter the image
    denoise = denoise_wavelet(filtered_audio, method='BayesShrink', mode='soft', wavelet_levels=3, wavelet='sym8',rescale_sigma='True')
    return list(denoise)

