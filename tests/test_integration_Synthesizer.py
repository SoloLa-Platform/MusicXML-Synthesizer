import pytest
from MusicXMLSynthesizer.Synthesizer import Synthesizer
from MusicXMLSynthesizer.utils import parse_notes_meta_to_list
from utility.testHelper import read_musicxml

# Integration Test (Generate output)
'''
    Integration test with real input data
'''

@pytest.mark.skip(reason="unstable input from solola can not validate Synthesizer")
def test_integration_real_input_bend():

    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    # input data
    techs_and_notes_list = parse_notes_meta_to_list(
        "input_audio/bend_solola/FinalNotes.txt")
    beats_list = parse_notes_meta_to_list(
        "input_audio/bend_madmom/beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "input_audio/bend_madmom/downbeats.txt")

    # setup
    synthesizer = Synthesizer(xsd_path)
    synthesizer.save(techs_and_notes_list, downbeats_list, beats_list)

    # prepare all the data we need
    beat_dur = synthesizer.calculate_beat_duration(
        "mode", synthesizer.extract_to_nparray(downbeats_list, [0])
    )
    first_downbeat_onset_list = synthesizer.get_frist_downbeats(downbeats_list)
    tech_and_notes_nparray = synthesizer.get_tech_and_notes_nparray(
        techs_and_notes_list)

    # synthesize musicXML
    synthesizer.execute('outputs/bend.musicxml')
    pass

@pytest.mark.skip(reason="unstable input from solola can not validate Synthesizer")
def test_integration_real_input_hammer_off():

    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    # input data
    techs_and_notes_list = parse_notes_meta_to_list(
        "input_audio/hammer_off_solola/FinalNotes.txt")
    beats_list = parse_notes_meta_to_list(
        "input_audio/hammer_off_madmom/beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "input_audio/hammer_off_madmom/downbeats.txt")

    # setup
    synthesizer = Synthesizer(xsd_path)
    synthesizer.save(techs_and_notes_list, downbeats_list, beats_list)

    # prepare all the data we need
    beat_dur = synthesizer.calculate_beat_duration(
        "mode", synthesizer.extract_to_nparray(downbeats_list, [0])
    )
    first_downbeat_onset_list = synthesizer.get_frist_downbeats(downbeats_list)
    tech_and_notes_nparray = synthesizer.get_tech_and_notes_nparray(
        techs_and_notes_list)

    # synthesize musicXML
    synthesizer.execute('outputs/hammer_off.musicxml')
    pass

@pytest.mark.skip(reason="unstable input from solola can not validate Synthesizer")
def test_integration_real_input_slide():
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    # input data
    techs_and_notes_list = parse_notes_meta_to_list(
        "input_audio/slide_solola/FinalNotes.txt")
    beats_list = parse_notes_meta_to_list(
        "input_audio/slide_madmom/beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "input_audio/slide_madmom/downbeats.txt")

    # setup
    synthesizer = Synthesizer(xsd_path)
    synthesizer.save(techs_and_notes_list, downbeats_list, beats_list)

    # prepare all the data we need
    beat_dur = synthesizer.calculate_beat_duration(
        "mode", synthesizer.extract_to_nparray(downbeats_list, [0])
    )
    first_downbeat_onset_list = synthesizer.get_frist_downbeats(downbeats_list)
    tech_and_notes_nparray = synthesizer.get_tech_and_notes_nparray(
        techs_and_notes_list)

    # synthesize musicXML
    synthesizer.execute('outputs/slide.musicxml')
    pass

@pytest.mark.skip(reason="unstable input from solola can not validate Synthesizer")
def test_integration_real_input_vibrato():
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    # input data
    techs_and_notes_list = parse_notes_meta_to_list(
        "input_audio/vibrato_solola/FinalNotes.txt")
    beats_list = parse_notes_meta_to_list(
        "input_audio/vibrato_madmom/beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "input_audio/vibrato_madmom/downbeats.txt")

    # setup
    synthesizer = Synthesizer(xsd_path)
    synthesizer.save(techs_and_notes_list, downbeats_list, beats_list)

    # prepare all the data we need
    beat_dur = synthesizer.calculate_beat_duration(
        "mode", synthesizer.extract_to_nparray(downbeats_list, [0])
    )
    first_downbeat_onset_list = synthesizer.get_frist_downbeats(downbeats_list)
    tech_and_notes_nparray = synthesizer.get_tech_and_notes_nparray(
        techs_and_notes_list)

    # synthesize musicXML
    synthesizer.execute('outputs/vibrato.musicxml')
    pass

'''
    integration test with mocked(ideal) solola input
'''
# @pytest.mark.skip(reason="under debugging with unit test")
def test_intergation_mocked_input_bend():
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    # input data
    techs_and_notes_list = parse_notes_meta_to_list(
        "input_mock/bend/FinalNotes.txt")
    beats_list = parse_notes_meta_to_list(
        "input_mock/bend/beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "input_mock/bend/downbeats.txt")
    # setup
    synthesizer = Synthesizer(xsd_path)
    synthesizer.save(techs_and_notes_list, downbeats_list, beats_list)

    # synthesize musicXML
    synthesizer.execute()

    result_musicxml = read_musicxml('outputs/bend/mocked_bend.musicxml')
    mocked_musicxml = read_musicxml('output_mock/bend/mocked_bend.musicxml')

    # assert result_musicxml == mocked_musicxml

    pass
