import pytest
from MusicXMLSynthesizer.Synthesizer import Synthesizer, read_raw_file

TESTCASE_ROOT_PATH = "/Users/ykhorizon/Workplace/projects/solola_project/musicxml-synthesizer/testcase"


def test_read_raw_file():

    # File path does not exist file
    # read single line
    TENT_str_list = read_raw_file(
        "{}/textfile1.txt".format(TESTCASE_ROOT_PATH))
    assert(TENT_str_list == ['abcde'])

# UNDONE


def test_sythesizer_parse():

    TENT_str_list = read_raw_file(
        "{}/case1_final_notes.txt".format(TESTCASE_ROOT_PATH))
    beats_str_list = read_raw_file(
        "{}/case1_beats.txt".format(TESTCASE_ROOT_PATH))

    syth = Synthesizer(TENT_str_list, beats_str_list)
    syth.create_musicXML_basic_template()


def test_calculate_solo_normalized_beat_duration():

    TENT_str_list = read_raw_file(
        "{}/case1_final_notes.txt".format(TESTCASE_ROOT_PATH))
    beats_str_list = read_raw_file(
        "{}/case1_beats.txt".format(TESTCASE_ROOT_PATH))

    syth = Synthesizer(TENT_str_list, beats_str_list)
    syth.calculate_solo_normalized_beat_duration()
    # no calculation occur
    assert(not(syth.beat_duration != -1))


def test_calcalate_solo_normalized_notes_duration():

    TENT_str_list = read_raw_file(
        "{}/case1_final_notes.txt".format(TESTCASE_ROOT_PATH))
    beats_str_list = read_raw_file(
        "{}/case1_beats.txt".format(TESTCASE_ROOT_PATH))

    syth = Synthesizer(TENT_str_list, beats_str_list)
    syth.calculate_solo_normalized_beat_duration("mode")
    # print(syth.beat_duration)
    syth.calcalate_solo_normalized_notes_duration()


@pytest.mark.skip(reason="no way of currently testing this, focus on xml buliding")
def test_set_musicXML_validator_by_xsd():

    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"
    TENT_str_list = read_raw_file(
        "{}/case1_final_notes.txt".format(TESTCASE_ROOT_PATH))
    beats_str_list = read_raw_file(
        "{}/case1_beats.txt".format(TESTCASE_ROOT_PATH))

    syth = Synthesizer(TENT_str_list, beats_str_list)

    syth.set_musicXML_validator_by_xsd(xsd_path)
