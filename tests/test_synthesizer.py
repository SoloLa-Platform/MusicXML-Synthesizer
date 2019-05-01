import pytest
from MusicXMLSynthesizer.Synthesizer import Synthesizer
from MusicXMLSynthesizer.utils import parse_notes_meta_to_list

TESTCASE_ROOT_PATH = "/Users/ykhorizon/Workplace/projects/solola_project/musicxml-synthesizer/testcase"


def test_parse_timing():

    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    # input data
    techs_and_notes_list = parse_notes_meta_to_list(
        "test_inputs/case1_final_notes.txt")
    beats_list = parse_notes_meta_to_list(
        "test_inputs/case1_beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "test_inputs/case1_downbeats.txt")
    syth = Synthesizer(xsd_path)
    syth.save(techs_and_notes_list, downbeats_list, beats_list)

    # prepare all the data we need
    beat_dur = syth.calculate_beat_duration(
        "mode", syth.extract_to_nparray(downbeats_list, [0])
    )
    first_downbeat_onset_list = syth.get_frist_downbeats(downbeats_list)
    tech_and_notes_nparray = syth.get_tech_and_notes_nparray(
        techs_and_notes_list)

    syth.execute();
    # syth.parse_timing(tech_and_notes_nparray,
    #                   first_downbeat_onset_list, beat_dur)
    # expect return format (order by time)
    # [[raw_onset, normalized_dur, raw_dur, type_str('n','r')]]
    pass


def test_plot_timing():
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"
    # input data
    techs_and_notes_list = parse_notes_meta_to_list(
        "test_inputs/case1_final_notes.txt")
    beats_list = parse_notes_meta_to_list(
        "test_inputs/case1_beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "test_inputs/case1_downbeats.txt")
    syth = Synthesizer(xsd_path)
    syth.save(techs_and_notes_list, downbeats_list, beats_list)

    
