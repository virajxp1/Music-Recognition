import os
import time
import cmath
import numpy as np
from audio2numpy import open_audio
import sounddevice as sd
from skimage.restoration import denoise_wavelet


# This file is used to get an mp3 input
# 2 functions
# a) to read from disk
# b) to read from input device


def read_file(filename, directory):
    filepath = os.path.join(directory, filename)
    audio, sampling_rate = open_audio(filepath)
    if len(audio.shape) > 1:
        audio = audio[:, 1:] + audio[:, :1]
        audio = [item for sublist in audio for item in sublist]
    # sd.play(audio,sampling_rate)
    # time.sleep(10)
    return audio, sampling_rate
