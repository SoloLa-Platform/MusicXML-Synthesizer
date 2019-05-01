# import madmom.features.downbeats
import madmom
import numpy as np
import sys


def beat_tracking(audioPath):
    proc = madmom.features.DBNDownBeatTrackingProcessor(beats_per_bar=[
        4, 4], fps=100)
    act = madmom.features.RNNDownBeatProcessor()(audioPath)
    # print(proc(act))
    beats = proc(act)
    return beats


def write_beats(beats, OUTPUT_PATH="downbeats.txt"):
    with open(OUTPUT_PATH, 'w') as f:
        for i, v in enumerate(beats):
            f.write("{},{}\n".format(v[0], v[1]))


if __name__ == '__main__':

    # song_path = 'Bohemian_Rhapsody_SOLO_Guitarraviva_normal_speed.wav'
    song_path = sys.argv[1]

    if song_path.split(".")[1] == 'wav' or song_path.split(".")[1] == 'WAV':
        downbeats = beat_tracking(song_path)
        print(downbeats)
        write_beats(downbeats)
    else:
        print("[Failed] The audio file is not .wav format, so it can not be conduct downbeat tracking algorithm!")
