import pytest
from MusicXMLSynthesizer.utils import parse_notes_meta_to_list
from MusicXMLSynthesizer.Synthesizer import Synthesizer
from utility.testHelper import create_synthesizer
import numpy as np


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
    print(result)

    assert np.alltrue(result == MOCKED_SOLOLA_OUTPUT)

# TODO: need more test input


def test_Synthesizer_annotate_start_end_edge():

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

    result = synthesizer.annotate_start_end_edge(
        MOCKED_SOLOLA_OUTPUT, MOCKED_FIRST_DOWNBEAT_LIST, MOCKED_DURATION)

    print(result)

    assert result == [[0.0, 'BS'], [0.0, 'NS'], [0.25, 'NE'], [0.25, 'NS'], [0.5, 'NE'], [0.5, 'NS'], [0.75, 'NE'], [0.75, 'NS'], [1.0, 'NE'], [1.0, 'BE'],
                      [1.0, 'BS'], [1.0, 'NS'], [1.25, 'NE'],  [1.25, 'NS'], [1.5, 'NE'], [1.5, 'NS'], [1.75, 'NE'], [1.75, 'NS'], [2.0, 'NE'], [2.0, 'BE'],
                      [2.0, 'BS'], [2.0, 'NS'], [2.25, 'NE'], [2.25, 'NS'], [2.5, 'NE'], [3.0, 'BE']]
    


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
    EDGE_ANNOTATED = [[0.0, 'BS'], [0.0, 'NS'], [0.25, 'NE'], [0.25, 'NS'], [0.5, 'NE'], [0.5, 'NS'], [0.75, 'NE'], [0.75, 'NS'], [1.0, 'NE'], [1.0, 'BE'],
                      [1.0, 'BS'], [1.0, 'NS'], [1.25, 'NE'],  [1.25, 'NS'], [1.5, 'NE'], [1.5, 'NS'], [1.75, 'NE'], [1.75, 'NS'], [2.0, 'NE'], [2.0, 'BE'],
                      [2.0, 'BS'], [2.0, 'NS'], [2.25, 'NE'], [2.25, 'NS'], [2.5, 'NE'], [3.0, 'BE']]
    synthesizer = create_synthesizer('input_mock/bend/')

    result = synthesizer.annotate_rest_and_technique(
        EDGE_ANNOTATED, MOCKED_SOLOLA_OUTPUT, MOCKED_FIRST_DOWNBEAT_LIST, MOCKED_DURATION)

    assert result == []
