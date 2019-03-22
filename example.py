from MusicXMLSynthesizer.Synthesizer import Synthesizer, parse_notes_meta_to_list

if __name__ == "__main__":

    TENT_string_list = parse_notes_meta_to_list(
        "testcase/case1_final_notes.txt")
    beats_string_list = parse_notes_meta_to_list("testcase/case1_beats.txt")
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"

    sy = Synthesizer(xsd_path)
    with open("./musicxml_example/hello_world.musicxml", "r") as fp:

        lines = fp.readlines()
        template_str = ""
        for l in lines:
            template_str += l.replace('\n', "").replace(" ", "")

        # initilize with customized template
        sy.set_base_xml(template_str)
        sy.execute(TENT_string_list, beats_string_list)
        # result = sy.execute(TENT_string_list, beats_string_list)
