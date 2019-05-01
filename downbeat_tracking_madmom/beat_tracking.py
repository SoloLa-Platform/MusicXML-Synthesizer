import madmom
import numpy as np
import sys


def beat_tracking(fp):
    
    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act =  madmom.features.beats.RNNBeatProcessor()(fp)
    # print(proc(act))
    beats = proc(act)
    return beats

def write_beats(beats, OUTPUT_PATH = "beats.txt"):

    with open(OUTPUT_PATH, 'w') as f:
        for i,v in enumerate(beats):
            f.write("{},{}\n".format(i,v))

if __name__ == '__main__':

    # song_path = 'Bohemian_Rhapsody_SOLO_Guitarraviva_normal_speed.wav'
    song_path = sys.argv[1]
    
    if song_path.split(".")[1] == 'wav' or  song_path.split(".")[1] == 'WAV':
        beats = beat_tracking(song_path)
        write_beats(beats)
    else:
        print("[Failed] The audio file is not .wav format, so it can not be conduct beat tracking algorithm!")
    

    


    
    