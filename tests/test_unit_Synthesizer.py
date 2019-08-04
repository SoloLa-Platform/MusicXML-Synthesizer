import pytest
from MusicXMLSynthesizer.utils import parse_notes_meta_to_list
from MusicXMLSynthesizer.Synthesizer import Synthesizer
from utility.testHelper import create_synthesizer
import numpy as np
from lxml import etree as ET

# 
# Naming convention: test_[CLASS_NAME]_[FUNCTION_NAME]_[CONDITION]
# 

def test_Synthesizer_calculate_beat_duration():
    MOCKED_DURATION = 0.25
    # setup
    synthesizer = create_synthesizer('input_mock/bend/')
    downbeats_list = parse_notes_meta_to_list(
        "input_mock/bend/downbeats.txt")

    beat_duration = synthesizer.calculate_beat_duration(
        "mode", synthesizer.extract_to_nparray(downbeats_list, [0])
    )

    assert beat_duration == MOCKED_DURATION


def test_Synthesizer_get_first_downbeats():
    MOCKED_FIRST_DOWNBEAT_LIST = [0.0, 1.0, 2.0, 3.0]
    # setup
    synthesizer = create_synthesizer('input_mock/bend/')
    downbeats_list = parse_notes_meta_to_list(
        "input_mock/bend/downbeats.txt")

    result = synthesizer.get_first_downbeat_edges(downbeats_list)

    assert result == MOCKED_FIRST_DOWNBEAT_LIST


def test_Synthesizer_get_tech_and_notes_nparray():

    MOCKED_SOLOLA_OUTPUT = np.array([
        [58,    0.,    0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.5,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.75,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.5,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.75,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    2.,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    2.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ], ])

    synthesizer = create_synthesizer('input_mock/bend/')
    techs_and_notes_list = parse_notes_meta_to_list(
        "input_mock/bend/FinalNotes.txt")

    result = synthesizer.get_tech_and_notes_nparray(techs_and_notes_list)

    assert np.alltrue(result == MOCKED_SOLOLA_OUTPUT)

# TODO: need more test input
def test_Synthesizer_annotate_start_end_edge_and_group_by_bar():

    MOCKED_FIRST_DOWNBEAT_LIST = [0.0, 1.0, 2.0, 3.0]
    MOCKED_SOLOLA_OUTPUT = np.array([
        [58,    0.,    0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.5,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.75,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.5,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.75,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    2.,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    2.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ], ])
    MOCKED_DURATION = 0.25
    synthesizer = create_synthesizer('input_mock/bend/')

    result = synthesizer.annotate_start_end_edge_and_group_by_bar(
        MOCKED_SOLOLA_OUTPUT, MOCKED_FIRST_DOWNBEAT_LIST, MOCKED_DURATION)

    assert result == [[[0.0, 'BS'], [0.0, 'NS'], [0.25, 'NE'], [0.25, 'NS'], [0.5, 'NE'], [0.5, 'NS'], [0.75, 'NE'], [0.75, 'NS'], [1.0, 'NE'], [1.0, 'BE']],
                      [[1.0, 'BS'], [1.0, 'NS'], [1.25, 'NE'],  [1.25, 'NS'], [1.5, 'NE'], [
                          1.5, 'NS'], [1.75, 'NE'], [1.75, 'NS'], [2.0, 'NE'], [2.0, 'BE']],
                      [[2.0, 'BS'], [2.0, 'NS'], [2.25, 'NE'], [2.25, 'NS'], [2.5, 'NE'], [3.0, 'BE']]]


def test_Synthesizer_annotate_rest_and_technique():
    MOCKED_FIRST_DOWNBEAT_LIST = [0.0, 1.0, 2.0, 3.0]
    MOCKED_SOLOLA_OUTPUT = np.array([
        [58,    0.,    0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.5,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    0.75,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.5,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    1.75,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    2.,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ],
        [58,    2.25,  0.25,  2,    0,    0,    0,    0,    0,    0,    0,    0, ], ])
    MOCKED_DURATION = 0.25
    EDGE_ANNOTATED = [[[0.0, 'BS'], [0.0, 'NS'], [0.25, 'NE'], [0.25, 'NS'], [0.5, 'NE'], [0.5, 'NS'], [0.75, 'NE'], [0.75, 'NS'], [1.0, 'NE'], [1.0, 'BE']],
                      [[1.0, 'BS'], [1.0, 'NS'], [1.25, 'NE'],  [1.25, 'NS'], [1.5, 'NE'], [
                          1.5, 'NS'], [1.75, 'NE'], [1.75, 'NS'], [2.0, 'NE'], [2.0, 'BE']],
                      [[2.0, 'BS'], [2.0, 'NS'], [2.25, 'NE'], [2.25, 'NS'], [2.5, 'NE'], [3.0, 'BE']]]
    synthesizer = create_synthesizer('input_mock/bend/')

    result = synthesizer.annotate_rest_and_technique(
        EDGE_ANNOTATED, MOCKED_SOLOLA_OUTPUT, MOCKED_FIRST_DOWNBEAT_LIST, MOCKED_DURATION)

    assert result == [[[4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]],
                      [[4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]],
                      [[4.0, 'n', 58.0, [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0,[2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [8.0, 'r']]]

# @pytest.mark.skip(reason="under debugging with unit test")
def test_Synthesize_solola_to_xml():
    ANNOTATED_DATA = [[[4.0, 'n', 58.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [4.0, 'n', 58.0,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]], [8.0, 'r']]]
    EXPECTED_RESULT = '''<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="3.1">
  <work>
    <work-title>solo</work-title>
  </work>
  <part-list>
    <score-part id="P1">
      <part-name>Music</part-name>
    </score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>16</divisions>
        <key>
          <fifths>0</fifths>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step>A</step>
          <alter>1</alter>
          <octave>3</octave>
        </pitch>
        <voice>1</voice>
        <duration>4.0</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>1</alter>
          <octave>3</octave>
        </pitch>
        <voice>1</voice>
        <duration>4.0</duration>
        <type>quarter</type>
      </note>
      <note>
        <rest/>
        <voice>1</voice>
        <duration>8.0</duration>
        <type>half</type>
      </note>
    </measure>
  </part>
</score-partwise>
'''
    synthesizer = create_synthesizer('input_mock/bend/')

    result = synthesizer.solola_to_xml(ANNOTATED_DATA)

    assert result == EXPECTED_RESULT
    
def test_Synthesize_createDurationType_standard_type():
    NOTE_El = ET.Element('note')
    DURATION = '4.0'

    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_duration_type(NOTE_El, DURATION)

    assert ET.tostring(NOTE_El, encoding="unicode") == '<note><type>quarter</type></note>'


def test_Synthesize_createDurationType_dot_type():
    NOTE_El = ET.Element('note')
    DURATION = '3.0'

    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_duration_type(NOTE_El, DURATION)

    assert ET.tostring(NOTE_El, encoding="unicode") == '<note><type>eighth</type><dot/></note>'


def test_Synthesize_createDurationType_abnormal_type():
    NOTE_El = ET.Element('note')
    DURATION = '15.0'

    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_duration_type(NOTE_El, DURATION)

    assert ET.tostring(NOTE_El, encoding="unicode") == '<note><type>non-standard</type></note>'


def test_Synthesize_add_technique_prebend():
    NOTE_El = ET.Element('note')
    TECHNIQUE = [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><bend><bend-alter>2</bend-alter><pre-bend/></bend></technical></notations></note>'


def test_Synthesize_add_technique_bend():
    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><bend><bend-alter>2</bend-alter></bend></technical></notations></note>'

def test_Synthesize_add_technique_release():
    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><bend><bend-alter>2</bend-alter><release/></bend></technical></notations></note>'

def test_Synthesize_add_technique_pull_off_start():

    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><pull-off type="start">P</pull-off></technical></notations></note>'

def test_Synthesize_add_technique_pull_off_stop():

    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><pull-off type="stop">P</pull-off></technical></notations></note>'


def test_Synthesize_add_technique_hammer_on_start():

    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><hammer-on type="start">H</hammer-on></technical></notations></note>'

def test_Synthesize_add_technique_hammer_on_stop():

    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><hammer-on type="stop">H</hammer-on></technical></notations></note>'


def test_Synthesize_add_technique_vibrato():

    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><other-technical><vibrato extent-level="1"/></other-technical></technical></notations></note>'

def test_Synthesize_add_technique_slide_start():
    
    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><slide type="start" line-type="solid"/></technical></notations></note>'


def test_Synthesize_add_technique_slide_stop():
    
    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><slide type="stop" line-type="solid"/></technical></notations></note>'


def test_Synthesize_add_technique_slidein():
    
    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><other-technical><slide-in from="below"/></other-technical></technical></notations></note>'


def test_Synthesize_add_technique_slideout():
    
    NOTE_El = ET.Element('note')
    TECHNIQUE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    synthesizer = create_synthesizer('input_mock/bend/')
    
    synthesizer.add_technique(NOTE_El, TECHNIQUE)

    assert ET.tostring(NOTE_El,encoding="unicode") == '<note><notations><technical><other-technical><slide-out direction="downward"/></other-technical></technical></notations></note>'
