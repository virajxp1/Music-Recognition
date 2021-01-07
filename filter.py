import time
from scipy import signal
from scipy.signal.signaltools import wiener
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


def audioFilter(audio,samplingrate):
    filtered_audio = wiener(audio)  # Filter the image
    # sd.play(filtered_audio,samplingrate)
    # time.sleep(10)
    return filtered_audio

