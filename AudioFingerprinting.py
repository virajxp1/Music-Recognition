import numpy as np

fuzzFactor = 4


def audio_fingerprint(audio, samplingrate):
    totalSize = len(audio)
    chunkSize = 4000
    sampledChunkSize = totalSize // chunkSize
    result = []

    for j in range(sampledChunkSize):
        complexArray = []
        for i in range(chunkSize):
            cmplx = complex(audio[(j * chunkSize) + i], 0)
            complexArray.append(cmplx)
        result.append(np.fft.fft(complexArray))

    highscores = np.zeros(shape = (len(result),5))
    points = np.zeros(shape = (len(result),5))
    fingerprint = []
    for t in range(len(result)):
        for freq in range(40, 300):
            mag = np.log(np.abs(result[t][freq]) + 1)
            index = getIndex(freq)

            if mag > highscores[t][index] :
                points[t][index] = freq
                highscores[t][index] = mag
        h = int(hash_func(points[t][0], points[t][1], points[t][2], points[t][3]))
        fingerprint.append(h)
    return fingerprint

# what needs to happen is that you return for the song a map that maps the hashtag of a chunk to the time stamp
# then to match u need to find the most matchings between the database and a sample input chunk

def getIndex(freq):
    Range = [40, 80, 120, 180, 300]
    i = 0
    while Range[i] < freq:
        i += 1
    return i


def hash_func(p1, p2, p3, p4):
    return (p4 - (p4 % fuzzFactor)) * 100000000+ (p3 - (p3 % fuzzFactor)) * 100000+ (p2 - (p2 % fuzzFactor)) * 100+ (p1 - (p1 % fuzzFactor));
