from pathlib import Path
from lxml import etree as ET
from MusicXMLSynthesizer.utils import parse_notes_meta_to_list
from MusicXMLSynthesizer.Synthesizer import Synthesizer


def read_musicxml(path):
    file_path = Path(path)
    if not file_path.is_file():
        print("Path:{}, Contnet: {}".format("Invalid", ""))
    else:
        tree = ET.parse(str(file_path))
        return ET.tostring(tree, xml_declaration=True,
                           encoding="UTF-8",doctype="""<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">""").decode("UTF-8")


def create_synthesizer(input_data_directory):
    # input data
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"
    techs_and_notes_list = parse_notes_meta_to_list(
        "{}FinalNotes.txt".format(input_data_directory))
    beats_list = parse_notes_meta_to_list(
        "{}beats.txt".format(input_data_directory))
    downbeats_list = parse_notes_meta_to_list(
        "{}downbeats.txt".format(input_data_directory))
    
    # setup
    synthesizer = Synthesizer(xsd_path)
    synthesizer.save(techs_and_notes_list, downbeats_list, beats_list)
    
    return synthesizer

