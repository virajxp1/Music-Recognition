import os
import time
import pandas as pd
from audio2numpy import open_audio
import sounddevice as sd
from GetInput import read_file
from AudioFingerprinting import audio_fingerprint
from AudioMatching import match
import datetime
import csv

# get input data -> fingerprint -> store
# get input test data -> fingerprint -> match
from filter import audioFilter


def buildData():
    # directory to our data
    dir = os.path.join(os.getcwd(), "corpus")
    # dir = os.path.join(os.getcwd(), "samples")
    AudioMappings = {}
    for file in os.listdir(dir):
        print("Building data for {}".format(file))
        audio, samplingrate = read_file(file, dir)
        fingerprint = audio_fingerprint(audio, samplingrate)
        AudioMappings[file] = fingerprint
    print("\n")

    # export data into a csv
    temp = []
    for key in AudioMappings:
        maping = AudioMappings[key]
        maping.append(key)
        temp.append(maping)
    with open("Database.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(temp)


def getSample():
    dir = os.path.join(os.getcwd(), "temp")
    sampleFingerprint = []
    sampleName = []
    for file in os.listdir(dir):
        audio, samplingrate = read_file(file, dir)
        audio = audioFilter(audio, samplingrate)
        sampleFingerprint.append(audio_fingerprint(audio, samplingrate))
        sampleName.append(file)
    return sampleFingerprint, sampleName


def getData():
    Database = {}
    with open('Database.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            d = row[0].split(',')
            name = d[-1]
            d = d[:-1]
            d = [int(i) for i in d]
            Database[name] = d
    return Database


def matchAudio_f():
    samples, sampleName = getSample()
    database = getData()
    i = 0
    for sample in samples:
        name = sampleName[i]
        matching_song = match(database, sample)
        print("Closest match for sample {} is {} ".format(name, matching_song))
        print("================== \n")
        i += 1


def printTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)


def matchAudio_ml():
    raise NotImplementedError

# buildData()
matchAudio_f()
