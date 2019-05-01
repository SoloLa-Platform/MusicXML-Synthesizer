from MusicXMLSynthesizer.Synthesizer import Synthesizer
from MusicXMLSynthesizer.utils import parse_notes_meta_to_list

if __name__ == "__main__":

    techs_and_notes_list = parse_notes_meta_to_list(
        "test_inputs/case1_final_notes.txt")
    beats_list = parse_notes_meta_to_list(
        "test_inputs/case1_beats.txt")
    downbeats_list = parse_notes_meta_to_list(
        "test_inputs/case1_downbeats.txt")
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    syth = Synthesizer(xsd_path)
    with open("./musicxml_example/hello_world.musicxml", "r") as fp:

        lines = fp.readlines()
        template_str = ""
        for l in lines:
            template_str += l.replace('\n', "").replace(" ", "")

        # initilize with customized template
        syth.create_musicXML_basic_template()
        # syth.plot_timing(20)
        # syth.prettyprintMzXML()
        syth.save(techs_and_notes_list, downbeats_list, beats_list)
        # syth.plot_timing()
        result = syth.execute()
