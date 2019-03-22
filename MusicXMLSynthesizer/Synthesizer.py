from pathlib import Path
from lxml import etree as ET
import numpy as np
from io import StringIO, BytesIO


class Synthesizer():

    def __init__(self, musicXML_schema_file_path):
        # default values
        self.beat_duration = -1
        self.score_part_XML_tree = None
        self.musicXML_schema = None

        # self.set_musicXML_validator_by_xsd(musicXML_schema_file_path)
    def set_base_xml(self, xml):
        self.score_part_XML_tree = xml

    def set_musicXML_validator_by_xsd(self, path):

        with open(path, "rb") as f:
            raw_xsd = f.read()
            xmlschema_doc = ET.parse(BytesIO(raw_xsd))
            self.musicXML_schema = ET.XMLSchema(xmlschema_doc)

    # PURPOSE: create a templace musicXML file
    # PARAMETERS: []
    # RETURN: []
    def create_musicXML_basic_template(self):

        root_score = ET.Element("score-partwise", version="3.1")
        root_score.append(ET.Element("movement-title"))
        root_score.append(ET.Element("identification"))
        root_score.append(ET.Element("part-list"))

        # part
        part = ET.Element("part", id="p1")

        # node in measure
        measure = ET.Element("measure", number="1")

        # attributes
        attr = ET.Element("attributes")

        # attributes/division
        divisions = ET.Element("divisions")
        divisions.text = "1"
        attr.append(divisions)

        # attributes/key
        key = ET.Element("key")

        fifths = ET.Element("fifth")
        fifths.text = "0"
        key.append(fifths)

        attr.append(key)

        # attributes/time
        time = ET.Element("time")

        beats = ET.Element("beats")
        beats.text = "4"
        beat_type = ET.Element("beat-type")
        beat_type.text = "4"
        time.append(beats)
        time.append(beat_type)

        attr.append(time)
        # attributes/clef
        clef = ET.Element("clef")

        sign = ET.Element("sign")
        sign.text = "G"
        line = ET.Element("line")
        line.text = "2"
        clef.append(sign)
        clef.append(line)
        attr.append(clef)

        measure.append(attr)

        part.append(measure)

        # append part
        root_score.append(part)

        # print(ET.tostring(root_score, pretty_print=True))
        self.score_part_XML_tree = root_score
        pass

    def execute(self, TENT_str_list, beats_str_list):
        if isinstance(TENT_str_list, list) and isinstance(beats_str_list, list):
            self.raw_TENT_final_notes = TENT_str_list
            self.raw_beats = beats_str_list
        else:
            print("TENT_str_list or beat_str_list is unprepared")
            return None

        # create default template
        if self.score_part_XML_tree is not "":
            self.create_musicXML_basic_template()

        # Calculate global information for whole song
        # duration/onset/pitch
        print("calculate_solo_normalized_beat_duration():")
        beat_duration = self.calculate_solo_normalized_beat_duration(
            "mode", self.parse_to_nparray(self.raw_beats)
        )
        print(beat_duration)

        print("calcalate_solo_normalized_notes_duration()")
        notes_duration_array_by_time_sequence = self.calcalate_solo_normalized_notes_duration(
            self.parse_to_list_of_tuple(
                self.raw_TENT_final_notes), beat_duration
        )
        print(notes_duration_array_by_time_sequence)
        # print("validate:{}".format(self.validate(self.score_part_XML_tree)))

    def validate(self, target_xml):
        # parse xml
        try:
            doc = self.musicXML_schema.validate(target_xml)
            print('XML well formed, syntax ok.')

        # check for file IO error
        except IOError:
            print('Invalid File')

        # check for XML syntax errors
        except ET.XMLSyntaxError as err:
            print('XML Syntax Error, see error_syntax.log')
            with open('error_syntax.log', 'w') as error_log_file:
                error_log_file.write(str(err.error_log))
            quit()

        except:
            print('Unknown error, exiting.')
            quit()

    def generate_from_soloLa(self):
        pass

    # PURPOSE: Read raw text file
    # PARAMETERS: cal_mode=[mode/mean].
    #   mode: use histogram to calculate most frequenct occur float number to decide beat duration
    #   mean: use average function to decide beat duration
    # RETURN:

    def parse_to_nparray(self, raw_beats_list):
        # Parse data input numpy array
        time = []
        for l in raw_beats_list:
            l_segment = l.replace('\n', '').split(",")
            time.append(float(l_segment[1]))

        # prepare two nparary
        return np.array(time)

    def parse_to_list_of_tuple(self, raw_TENT_final_note):
        return [tuple(map(float, l.replace(
            "\n", "").split(" ")))for l in raw_TENT_final_note]

    def calculate_solo_normalized_beat_duration(self, cal_mode="mode", raw_beats_nparray=None):
        if raw_beats_nparray is None:
            return

        raw_duration = np.delete(raw_beats_nparray, 0) - \
            np.delete(raw_beats_nparray, raw_beats_nparray.size-1)

        result = None
        if cal_mode == "mode":
            # mode number
            distr = np.histogram(raw_duration, bins=10)
            max_index = np.argmax(distr[0])
            result = distr[1][max_index]

        elif cal_mode == "mean":
            result = np.mean(raw_duration)

        return result

    def calcalate_solo_normalized_notes_duration(self, TENT_list_of_tuple_data, beat_duration):

        # parse note
        # read duration in final_note
        # normalize with beat unit duration (division / multiple)

        # print(list_of_tuple_data)
        self.num_TENT_final_notes = np.asarray(TENT_list_of_tuple_data)
        notes_duration = self.num_TENT_final_notes[:, 2]/beat_duration
        print("np.histogram")
        print(np.histogram(notes_duration, bins=16))
        return notes_duration

    def transform_note_picth_by_C_major(self):
        # default use C major
        # call a map tranfer midi pitch num. to letter name
        pass

    def transform_raw_note_into_musicXML(self):

        # calculate_solo_normalized_beat_duration()
        # calcalate_solo_normalized_notes_duration(), calculate global note division/multiple
        #
        # iterate note element with final_note results
        #   1. tranform note duration (mapping)
        #   2. tranform note pitch (mapping)
        #   3. tranform note tech (mapping)
        #   4. Create musicXML note element and append propropties
        #   5. append musicXML note to full-musicXML doc

        pass


#
#   Utility function
#

# PURPOSE: Read raw text file
# PARAMETERS: [file_path]
# RETURN: [string[]]


def parse_notes_meta_to_list(file_path):

    result_list = []
    # detect non-exist file path
    fp = Path(file_path)
    if not fp.is_file():
        print("Path:{}, Contnet: {}".format("Invalid", ""))
    with open(file_path, 'r') as f:
        result_list = f.readlines()

    return result_list
