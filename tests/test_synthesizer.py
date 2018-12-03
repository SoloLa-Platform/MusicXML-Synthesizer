
from MusicXMLSynthesizer.Synthesizer import Synthesizer,read_raw_file

TESTCASE_ROOT_PATH = "/Users/ykhorizon/Workplace/projects/solola_project/musicxml-synthesizer/testcase"


def test_read_raw_file():
    
    # File path does not exist file
    # read single line
    TENT_str_list = read_raw_file("{}/textfile1.txt".format(TESTCASE_ROOT_PATH))
    assert(TENT_str_list == ['abcde'])


def test_sythesizer_constructor():

    # [Assign single lines list]
    syth = Synthesizer(["abc"],["def"])
    assert( syth.raw_TENT_final_notes == ["abc"] )
    assert( syth.raw_beats == ["def"] )
    
    # [Assign muliple lines]
    
    # [Todo][Assign Non-list type]
    # design a protection mechanism to catch exception
    syth = Synthesizer("abc","abc")

# UNDONE
def test_sythesizer_parse():
    
    TENT_str_list = read_raw_file("{}/case1_final_notes.txt".format(TESTCASE_ROOT_PATH))
    beats_str_list = read_raw_file("{}/case1_beats.txt".format(TESTCASE_ROOT_PATH))
    
    syth = Synthesizer(TENT_str_list,beats_str_list)
    syth.create_musicXML_basic_template()

    
def test_calculate_beat_duration():

    TENT_str_list = read_raw_file("{}/case1_final_notes.txt".format(TESTCASE_ROOT_PATH))
    beats_str_list = read_raw_file("{}/case1_beats.txt".format(TESTCASE_ROOT_PATH))
    
    syth = Synthesizer(TENT_str_list,beats_str_list)
    syth.calculate_beat_duration()
    # no calculation occur
    assert(not(syth.beat_duration != -1))
    

