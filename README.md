# MusicXML-Synthesizer

This program is still under development and test.

A program can convert solola output to musicXML(.musicxml) format
[Solola output] => MusicXML-Synthesizer => [musicxml format file]

Note: We will set [MuseScore](https://github.com/musescore/MuseScore) as validation editor. It means that MusicXML-Synthesizer will ensure output can be successfully opened
by [MuseScore](https://github.com/musescore/MuseScore)

# Appendix
## SoloLa output format (Input)
  Example:
      (0)    (1)   (2)   (3)   (4)   (5)   (6)   (7)   (8)   (9)  (10)  (11)
      
      Pit     On   Dur  PreB     B     R     P     H     S    SI    SO     V    
      
  [    66   1.24   0.5     2     0     0     0     0     1     2     1     1]
  
  Pit:    pitch (MIDI number)
  On:     onset (sec.)
  Dur:    duration (sec.)
  PreB:   pre-bend (0 for none,
                    1 for bend by 1 semitone,
                    2 for bend by 2 semitone,
                    3 for bend by 3 semitone)

  B:      string bend (0 for none,
                       1 for bend by 1 semitone,
                       2 for bend by 2 semitone,
                       3 for bend by 3 semitone)

  R:      release  (0: none, 
                    1: release by 1 semitone,
                    2: release by 2 semitone,
                    3: release by 3 semitone)

  P:      pull-off (0: none, 
                    1: pull-off start,
                    2: pull-off stop)

  H:      hammer-on (0: none,
                     1: hammer-on start,
                     2: hammer-on stop)

  S:      legato slide (0: none,
                        1: legato slide start, 
                        2: legato slide stop)
              
  SI:     slide in (0: none,
                    1: slide in from below,
                    2: slide in from above)

  SO:     slide out (0: none,
                     1: slide out downward,

## musicXMl (Output)
[musicXML example](https://www.musicxml.com/publications/makemusic-recordare/notation-and-analysis/a-sample-musicxml-encoding/)
