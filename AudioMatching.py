import numpy as np


def match_std(database, sample):
    std_differences = []
    n = len(sample)
    for song in database:
        song_fingerprint = database[song]
        differences = []
        timeStamped_dif = []
        # print("Matching with song: {}".format(song))
        for i in range(len(song_fingerprint) - n + 1):
            difference = np.subtract(song_fingerprint[i:n + i], sample)
            differences.append(np.abs((sum(difference))))
            timeStamped_dif.append((np.abs((sum(difference))), i))
        timeStamped_dif.sort(key=lambda tup: tup[0])  # sorts in place
        timeStamped_dif = timeStamped_dif[:4]
        dif, ts = zip(*timeStamped_dif)
        std_differences.append((np.std(ts), song))
        # print("Standard Deviation of the top 3 time stamps is {}".format(np.std(ts)))
    return std_differences


# adding time stamps to above approach - add each difference with time stamp - then sort by differences
# on 6 samples:
# 50% accurate - no time stamps looking at mean vs min difference
# 55% 5/9 accurate - with time stamps

# alternative approach you can iterate through all chunks in the sample and find each point with smallest difference
# append the difference and time stamp them and then look at the array of the top n - length of sample differences
# idk maybe take the average of the time stamps and then find pick the one with the smallest standard deviation
# 66% 6/9 accurate


def match_ic(database, sample):
    song_scores = []
    for song in database:
        song_data = database[song]
        smallest_diff = []  # difference between sample chunk and song chunk with time stamps of the song
        for sample_chunk in sample:
            i = 0
            local_mindif = [np.inf, 0]
            for song_chunk in song_data:
                difference = np.abs(sample_chunk - song_chunk)
                if difference < local_mindif[0]:
                    local_mindif[0] = difference
                    local_mindif[1] = i
                i += 1
            smallest_diff.append(tuple(local_mindif))
        smallest_diff.sort(key=lambda tup: tup[0])  # sorts in place
        # mean of difference tells u how far apart each chunk is to song
        # standard deviation of time stamps tells u how far way each time stamp is from each other
        # large standard deviation means matches are really far apart
        d, ts = zip(*smallest_diff)
        mean_of_differences = np.mean(d)
        smallest_diff = [i for i in smallest_diff if i[0] <= mean_of_differences]
        d, ts = zip(*smallest_diff)
        ts = list(ts)
        ts.sort()
        score = (.9 * mean_of_differences) + (.2 * np.std(ts))
        # print( "The mean of differences is {} the standard deviation of time stamps is {} for song {} with a score
        # of {}".format( mean_of_differences, np.std(ts), song, score))
        song_scores.append((score, song))
    return song_scores


def match_shz(database, sample):
    song_scores = []
    for song in database:
        song_data = database[song]
        j = 0
        difis0_timestamps = []
        for sample_chunk in sample:
            i = 0
            for song_chunk in song_data:
                if sample_chunk == song_chunk:
                    difis0_timestamps.append((j, i))  # ( sample time stamp , song time stamp )
                i += 1
            j += 1
        matches = 0
        for songts_i, samplets_i in difis0_timestamps:
            for songts_j, samplets_j in difis0_timestamps:
                if np.abs(songts_i - songts_j) == np.abs(samplets_i - samplets_j):
                    matches += 1
        # print("number of matches =  {}".format(matches))
        song_scores.append((matches, song))
    return song_scores


# take sample chunk x and song chunk y if there is a match -> add it to the matches and put timestamp of both sample
# and song double for loop take each for each match compare with all other matches and when timestamps match up add
# it as a hit* song with maximum number of hits wins

def match(database, sample):
    scores1 = match_ic(database, sample)
    scores2 = match_std(database, sample)
    scores3 = match_shz(database, sample)
    scores1.sort(key=lambda tup: tup[0])
    scores2.sort(key=lambda tup: tup[0])
    scores3.sort(key=lambda tup: tup[0])
    scores3.reverse()

    # print("individual chunks: ", scores1)
    # print("minimum standard deviation : ", scores2)
    # print("using time stamp matching : ", scores3)

    songRankings = getBestSong(scores1, scores2, scores3)
    return songRankings[0][0]


def getBestSong(scores1, scores2, scores3):
    songRankings = {}
    n = len(scores1)
    i = 0
    for score, song in scores1:
        songRankings[song] = i
        if i < 3:
            i += 1
    i = 0
    for score, song in scores2:
        songRankings[song] += i
        if i < 3:
            i += 1
    i = 0
    for score, song in scores3:
        songRankings[song] += i
        if i < 3:
            i += 1
    for song in songRankings:
        songRankings[song] = (songRankings[song] / n)

    songRankings = list(sorted(songRankings.items(), key=lambda item: item[1]))
    print(songRankings[:3])
    return songRankings


def getOriginalityIndex():
    return 0
