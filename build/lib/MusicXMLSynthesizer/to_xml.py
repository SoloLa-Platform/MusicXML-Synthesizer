def generate_structured_data(self, measures, downbeats,  beat_duration, tech_and_notes_nparray):
    note_index = 0
    downbeat_index = 0
    measure_index = 0
    for measure in measures:
        
        measureEl = ET.Element('measure')
        # Generate a raw data structure for note with tech
        # Generate mzxml file
        note_dict = {'pitch': '', 'pitch_raw': 0,
                        'onset': 0, 'onset_raw': 0,
                        'dur': 0, 'dur_raw': 0
                        }
        # note is unique onset value
        for noteOnset in measure:
            # Check if need to add rest 
            db_onset = downbeats[downbeat_index][1]
            # an ignorable gap between first downbeat and note
            if noteOnset - db_onset < (beat_duration/16):
                downbeat_index += 1
            # an rest between note and downbeatㄍㄟ
            elif noteOnset - db_onset >= (beat_duration/16):
                rest_dur = self.note_based_normalize_to_4beat_per_measure(
                    noteOnset - db_onset)/(beat_duration/16)
                print('rest: {}'.format(rest_dur))
            # if is rest, o2-(o1+d1) > (beat_duration/16), o=onset, d=duration
            # if note_index < len(tech_and_notes_nparray):
            # Add note
            noteEl = ET.Element('note')
            # Select row of specific note with tech by onset
            index = np.where(
                tech_and_notes_nparray[:, ONSET_INDEX] == noteOnset)

            # Normalized picth and Add element
            # note_dict['pitch_raw'] = tech_and_notes_nparray[index,
            #                                                 PITCH_INDEX][0][0]
            # note_dict['pitch'] = self.convert_midi_num_to_note_name(
            #     int(tech_and_notes_nparray[index, PITCH_INDEX]))
            pitch = self.convert_midi_num_to_note_name(
                int(tech_and_notes_nparray[index, PITCH_INDEX]))
            pitchEl = ET.Element('pitch')
            stepEl = ET.Element('step')
            stepEl.text = pitch[0]
            
            octaveEl = ET.Element('octave')
            if len(pitch) == 3 and pitch[1] == '#':
                alterEl = ET.Element('alter')
                alterEl.text = '1'
                pitchEl.append(alterEl)
                octaveEl.text = pitch[2]
            elif len(pitch) == 2:
                octaveEl.text = pitch[1]
            
            pitchEl.append(stepEl)
            pitchEl.append(octaveEl)


            # Add duration & voice & type
            normalized_duration = tech_and_notes_nparray[index,
                                                        DUR_INDEX] / beat_duration
            final_dur = self.note_based_normalize_to_4beat_per_measure(
                normalized_duration)*4
            print('note: {}'.format(str(final_dur)))
            durationEl = ET.Element('duration')
            durationEl.text = str(final_dur)

            durTypeEl = ET.Element('type')
            # durTypeEl.text = DUR_TYPE[final_dur]

            noteEl.append(pitchEl)
            noteEl.append(durationEl)
            noteEl.append(durTypeEl)

            #(2) Add tech

            # print(note_dict)
            note_index += 1

