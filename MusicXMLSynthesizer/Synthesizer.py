# import matplotlib.pyplot as plt
import pretty_midi
import math
from pathlib import Path
from lxml import etree as ET, objectify
from lxml.etree import XMLSyntaxError, fromstring
import numpy as np
from io import StringIO, BytesIO
from operator import itemgetter
import matplotlib
matplotlib.use('TkAgg')

PITCH_INDEX = 0
ONSET_INDEX = 1
DUR_INDEX = 2
DUR_TYPE = {'16.0': 'whole', '8.0': 'half',
            '4.0': 'quarter', '2.0': 'eighth', '1.0': '16th'}

VALUE_INDEX = 0
TYPE_INDEX = 1


class Synthesizer():

    def __init__(self, schema_path):
        # default values
        self.beat_duration = -1
        self.mzxml = None
        self.schema_path = schema_path



    def save(self, techs_and_notes_list, downbeats_str_list, beat_str_list):
        if isinstance(techs_and_notes_list, list) and isinstance(beat_str_list, list) and isinstance(downbeats_str_list, list):
            self.raw_tech_and_notes = techs_and_notes_list
            self.raw_beats = beat_str_list
            self.raw_downbeats = downbeats_str_list
        else:
            print("techs_and_notes_list or beat_str_list is unprepared")
            return None

    def write_file(self, path="./output.musicxml", content=""):
        file = open(path, "w+")
        file.write(content)

    def execute(self):
        beat_duration = self.calculate_beat_duration(
            "mode", self.extract_to_nparray(self.raw_downbeats, [0])
        )
        first_downbeat_onset_list = self.get_frist_downbeats(
            self.raw_downbeats)
        # downbeat_onset_list = self.get_downbeats(self.raw_downbeats)
        tech_and_notes_nparray = self.get_tech_and_notes_nparray(
            self.raw_tech_and_notes)
        
        solola_format_data = self.parse_timing(tech_and_notes_nparray,
                                               first_downbeat_onset_list, beat_duration)

        xml = self.solola_to_xml(solola_format_data, "My awesome solo sheet")
        self.write_file('output.musicxml', xml)

    def parse_to_list_of_tuple(self, target_list):
        return [tuple(map(float, l.replace(
            "\n", "").split(" ")))for l in target_list]

    def get_tech_and_notes_nparray(self, raw_tech_and_notes):
        return np.asarray(
            self.parse_to_list_of_tuple(raw_tech_and_notes))

    def calculate_beat_duration(self, cal_mode="mode", raw_beats_nparray=None):
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

    def get_frist_downbeats(self, raw_downbeats):
        first_downbeat_onset_list = []
        for item in self.raw_downbeats:
            value_list = item.rstrip("\n").split(",")
            if value_list[1] == "1.0":
                first_downbeat_onset_list.append(float(value_list[0]))
        first_downbeat_onset_list.insert(0, 0)
        return first_downbeat_onset_list

    def get_downbeats(self, raw_downbeats):
        downbeat_onset_list = []
        for item in self.raw_downbeats:
            value_list = item.rstrip("\n").split(",")
            if value_list[1] == "1.0":
                downbeat_onset_list.append(
                    (float(value_list[0]), float(value_list[1])))
        return downbeat_onset_list

    def parse_timing(self, tech_and_notes_nparray, first_downbeat_onset_list, beat_duration):
        # first_downbeat_onset_list: aims to identify measure(bar)
        # beat_duration: normalized note minumum duration 1/16 in second unit
        print("beat_duration: {}".format(beat_duration))
        solo_measures = []
        measure_index = 0
        onset = tech_and_notes_nparray[:, ONSET_INDEX]
        dur = tech_and_notes_nparray[:, DUR_INDEX]
        edge_last_to_next = []
        solola_formated_total = []
        while measure_index < len(first_downbeat_onset_list)-1:

            start = first_downbeat_onset_list[measure_index]
            end = first_downbeat_onset_list[measure_index+1]

            # Find the notes in same measure by downbeat
            notes_in_measure = onset[(start < onset) & (onset <= end)]
            mapped_dur = dur[(start < onset) & (onset <= end)]

            # print("notes_in_measure: ", notes_in_measure, "dur:",
            #       mapped_dur, "({},{})".format(start, end))

            total = notes_in_measure.tolist()
            typed_total = []

            # Add previous measure node ending
            typed_total += edge_last_to_next
            edge_last_to_next = []

            # add start of measture as edge
            typed_total.insert(0, [start, 'ds'])

            # Add ending timing of note to typed_total
            note_index = 0
            while note_index < len(total):
                # add note onset as e1
                e1 = notes_in_measure[note_index]
                typed_total.append([e1, 'no'])

                # add note end timing as e2
                e2 = notes_in_measure[note_index] + mapped_dur[note_index]
                if e2 > end:
                    edge_last_to_next.append([e2, 'ne'])
                else:
                    typed_total.append([e2, 'ne'])
                note_index += 1

            # add end of measture as edge
            typed_total.append([end, 'de'])
            # print('typed:', typed_total)

            # iterate all the edge point (included downbeat) in measure
            total_index = 0
            solola_formated_measure = []
            while total_index < len(typed_total)-1:
                # print(total_index)
                e1 = typed_total[total_index]
                e2 = typed_total[total_index+1]

                # same edge (ne from previous measure may be equal to no in current measure)
                if e1[VALUE_INDEX] == e2[VALUE_INDEX]:
                    total_index += 1
                    continue

                # Check e1 to e2 is a rest
                if (e1[TYPE_INDEX] == 'ds' and e2[TYPE_INDEX] == 'no') or (e1[TYPE_INDEX] == 'ne' and e2[TYPE_INDEX] == 'de'):
                    rest_dur = round((e2[VALUE_INDEX] -
                                      e1[VALUE_INDEX])/(beat_duration/4))
                    if rest_dur > 1:
                        solola_formated_measure.append([rest_dur, 'r'])

                # Check e1 to e2 is a note
                if (e1[TYPE_INDEX] == 'no' and e2[TYPE_INDEX] == 'ne') or (e1[TYPE_INDEX] == 'no' and e2[TYPE_INDEX] == 'de'):
                    # 1/16
                    note_dur = round((e2[VALUE_INDEX] -
                                      e1[VALUE_INDEX])/(beat_duration/4))
                    if note_dur > 1:
                        tech = tech_and_notes_nparray[e1[VALUE_INDEX] == onset, 3:12].tolist()[
                            0]
                        pitch = tech_and_notes_nparray[e1[VALUE_INDEX]
                                                       == onset, 0]
                        is_non_tech_note = all(v == 0.0 for v in tech)
                        if is_non_tech_note:
                            solola_formated_measure.append(
                                [note_dur, 'n', pitch[0], []])
                        else:
                            solola_formated_measure.append(
                                [note_dur, 'n', pitch[0], tech])

                total_index += 1
            
            print(len(solola_formated_measure), solola_formated_measure)
            solola_formated_total.append(solola_formated_measure)
            # print('total:', solola_formated_total)
            # print()

            measure_index += 1
 
        return solola_formated_total

    def solola_to_xml(self, solola_formated_data, sheet_title="solo"):
        # top root
        scorewiseEl = ET.Element('score-partwise', version="3.1")

        workEl = ET.Element('work')
        workTitleEl = ET.Element('work-title')
        workTitleEl.text = sheet_title
        workEl.append(workTitleEl)
        scorewiseEl.append(workEl)

        # identificationEl = ET.Element('identification')
        # scorewiseEl.append(identificationEl)

        # defaultsEl = ET.Element('defaults')
        # scorewiseEl.append(defaultsEl)

        # creditEl = ET.Element('credit')
        # scorewiseEl.append(creditEl)
        
        # part
        partId = 1
        partListEl = ET.Element('part-list')
        scorePartEl = ET.Element('score-part', id="P{}".format(str(partId)))
        partNameEl = ET.Element('part-name')
        partNameEl.text = 'Music'
        scorePartEl.append(partNameEl)
        partListEl.append(scorePartEl)
        scorewiseEl.append(partListEl)

        partEl = ET.Element('part', id="P{}".format(str(partId)))
        
        for measure in solola_formated_data:
            SOLOLA_DUR = 0
            SOLOLA_TYPE = 1
            SOLOLA_PITCH = 2
            measureEl = ET.Element('measure', number=str(partId))
            attrEl = self.attr_factory()
            measureEl.append(attrEl)
            # entity include note and rest
            for entity in measure:
                noteEl = ET.Element('note')
                dur = str(entity[SOLOLA_DUR])
                if entity[SOLOLA_TYPE] == 'n':
                    # pitch
                    pitchEl = ET.Element('pitch')
                    stepEl = ET.Element('step')
                    pitch_value = self.convert_midi_num_to_note_name(
                        entity[SOLOLA_PITCH])
                    stepEl.text = pitch_value[0]
                    pitchEl.append(stepEl)

                    octaveEl = ET.Element('octave')
                    if len(pitch_value) == 3 and pitch_value[1] == '#':
                        alterEl = ET.Element('alter')
                        alterEl.text = '1'
                        pitchEl.append(alterEl)
                        octaveEl.text = pitch_value[2]
                    elif len(pitch_value) == 2:
                        octaveEl.text = pitch_value[1]

                    
                    pitchEl.append(octaveEl)
                    noteEl.append(pitchEl)

                    # duration
                    durEl = ET.Element('duration')
                    durEl.text = dur
                    noteEl.append(durEl)

                    # voice
                    voiceEl = ET.Element('voice')
                    voiceEl.text = '1'
                    noteEl.append(voiceEl)

                    # type(duration)
                    durTypeEl = ET.Element('type')
                    # handle with dot duration (3, 6, 12)
                    if dur in ['3.0', '6.0', '12.0']:
                        if dur == '3.0':
                            durTypeEl.text = DUR_TYPE['2.0']
                        elif dur == '6.0':
                            durTypeEl.text = DUR_TYPE['4.0']
                        elif dur == '12.0':
                            durTypeEl.text = DUR_TYPE['8.0']
                        noteEl.append(durTypeEl)
                        # dot env
                        dotEl = ET.Element('dot')
                        noteEl.append(dotEl)
                    # uncommon duration type
                    elif dur in ['15.0', '14.0', '13.0', '11.0', '10.0', '9.0', '7.0', '5.0']:
                        durTypeEl.text = 'non-standard'
                        noteEl.append(dotEl)

                    # DUR_TYPE = {'16.0': 'whole', '8.0': 'half', '4.0': 'quarter', '2.0': 'eighth', '1.0': '16th'}
                    else:
                        durTypeEl.text = DUR_TYPE[dur]
                        noteEl.append(durTypeEl)

                elif entity[SOLOLA_TYPE] == 'r':
                    # rest
                    restEl = ET.SubElement(noteEl, 'rest')
                    noteEl.append(restEl)

                    # duration
                    durEl = ET.Element('duration')
                    durEl.text = dur
                    noteEl.append(durEl)

                    # voice
                    voiceEl = ET.Element('voice')
                    voiceEl.text = '1'
                    noteEl.append(voiceEl)

                    # type(duration)
                    durTypeEl = ET.Element('type')
                    # handle with dot duration (3, 6, 12)
                    if dur in ['3.0', '6.0', '12.0']:
                        if dur == '3.0':
                            durTypeEl.text = DUR_TYPE['2.0']
                        elif dur == '6.0':
                            durTypeEl.text = DUR_TYPE['4.0']
                        elif dur == '12.0':
                            durTypeEl.text = DUR_TYPE['8.0']
                        noteEl.append(durTypeEl)
                        # dot env
                        dotEl = ET.Element('dot')
                        noteEl.append(dotEl)
                    # uncommon duration type
                    elif dur in ['15.0', '14.0', '13.0', '11.0', '10.0', '9.0', '7.0', '5.0']:
                        durTypeEl.text = 'non-standard'
                        noteEl.append(dotEl)

                    # DUR_TYPE = {'16.0': 'whole', '8.0': 'half', '4.0': 'quarter', '2.0': 'eighth', '1.0': '16th'}
                    else:
                        durTypeEl.text = DUR_TYPE[dur]
                        noteEl.append(durTypeEl)

                measureEl.append(noteEl)
            partEl.append(measureEl)

            partId += 1

        scorewiseEl.append(partEl)
        # return ET.tostring(scorewiseEl, pretty_print=True)
        return ET.tostring(scorewiseEl, pretty_print=True, xml_declaration=True,
                           encoding="UTF-8",
                           doctype="""<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">""").decode("utf-8")

    def convert_midi_num_to_note_name(self, midi_num):
        # midi note number & note name
        # https://newt.phys.unsw.edu.au/jw/notes.html
        if midi_num < 21 or midi_num > 108:
            return ""
        else:
            return pretty_midi.note_number_to_name(int(midi_num))

    def note_based_normalize_to_4beat_per_measure(self, note_duration):
        value = 0
        if (note_duration <= 0.25) or (note_duration > 0.25 and note_duration <= 0.375):
            value = 0.25
        elif note_duration > 0.375 and note_duration <= 0.75:
            value = 0.5
        elif note_duration > 0.75 and note_duration <= 1.25:
            value = 1
        elif note_duration > 1.25 and note_duration <= 1.75:
            value = 1.5
        else:
            value = math.floor(note_duration)
        return value

    def extract_to_nparray(self, raw_beats_list, extract_index_list):
        if len(raw_beats_list) < 1:
            return np.array([])
        colume_num = len(raw_beats_list[0].replace('\n', '').split(","))
        # print(colume_num)
        if len(extract_index_list) == 0:
            return np.array([])
        time = []
        for l in raw_beats_list:
            l_segment = l.replace('\n', '').split(",")
            time.append(float(itemgetter(*extract_index_list)(l_segment)))

        return np.array(time)

    def plot_timing(self, controlled_count):
        beat_duration = self.calculate_beat_duration(
            "mode", self.extract_to_nparray(self.raw_downbeats, [0])
        )
        first_downbeat_onset_list = self.get_frist_downbeats(
            self.raw_downbeats)
        # downbeat_onset_list = self.get_downbeats(self.raw_downbeats)
        tech_and_notes_nparray = self.get_tech_and_notes_nparray(
            self.raw_tech_and_notes)

        # tech_and_notes_nparray
        x = np.linspace(0, 2, 100)
        count = 0
        for data_row in tech_and_notes_nparray:
            if count == controlled_count:
                break
            plt.plot([data_row[1], data_row[1]+data_row[2]],
                     [data_row[0], data_row[0]])
            count += 1

        plt.xlabel('timing(sec)')
        plt.ylabel('pitch(midi num)')
        plt.title("Plot note by onset and duration")
        plt.legend()
        plt.show()

    def validate(self, target_string):
        try:
            schema = ET.XMLSchema(file=self.self.schema_path)
            parser = objectify.makeparser(schema=schema)
            objectify.fromstring(target_string, parser)
            return True

        except XMLSyntaxError:
            
            return False

    #
    #  xml node generation factory
    #
    def divisions_factory(self, number=16):
        divisions = ET.Element("divisions")
        divisions.text = str(number)
        return divisions

    def key_factory(self):
        key = ET.Element("key")
        fifths = ET.Element("fifths")
        fifths.text = "0"
        key.append(fifths)
        return key

    def time_factroy(self):
        time = ET.Element("time")
        beats = ET.Element("beats")
        beats.text = "4"
        beat_type = ET.Element("beat-type")
        beat_type.text = "4"
        time.append(beats)
        time.append(beat_type)
        return time

    def clef_factory(self):
        clef = ET.Element("clef")
        sign = ET.Element("sign")
        sign.text = "G"
        line = ET.Element("line")
        line.text = "2"
        clef.append(sign)
        clef.append(line)
        return clef

    def attr_factory(self):
        # attributes
        attr = ET.Element("attributes")

        # attributes/division
        attr.append(self.divisions_factory())

        # attributes/key
        attr.append(self.key_factory())

        # attributes/time
        attr.append(self.time_factroy())

        # attributes/clef
        attr.append(self.clef_factory())
        return attr

    #
    # unused part
    #

    def create_musicXML_basic_template(self):

        root_score = ET.Element("score-partwise", version="3.1")
        root_score.append(ET.Element("movement-title"))
        root_score.append(ET.Element("identification"))
        root_score.append(ET.Element("part-list"))

        # part
        part = ET.Element("part", id="p1")

        # node in measure
        measure = ET.Element("measure", number="1")
        measure.append(self.attr_factory())
        part.append(measure)

        # append part
        root_score.append(part)
        self.mzxml = root_score

    def get_onsets_grouped_by_measure(self, tech_and_notes_nparray, first_downbeat_onset_list):
        solo_measures = []
        measure_index = 0
        onset = tech_and_notes_nparray[:, ONSET_INDEX]
        dur = tech_and_notes_nparray[:, DUR_INDEX]
        while measure_index < len(first_downbeat_onset_list)-1:
            # Find the notes in same measure by downbeat
            measure = onset[(
                first_downbeat_onset_list[measure_index] < onset) &
                (onset <= first_downbeat_onset_list[measure_index+1])]
            mapped_dur = dur[(
                first_downbeat_onset_list[measure_index] < onset) &
                (onset <= first_downbeat_onset_list[measure_index+1])]

            # print(measure, mapped_dur, '({},{})'.format(
            #     first_downbeat_onset_list[measure_index],
            #     first_downbeat_onset_list[measure_index+1]))
            solo_measures.append(measure)
            measure_index += 1
        return solo_measures
