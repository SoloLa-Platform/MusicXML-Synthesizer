from pathlib import Path
from lxml import etree as ET
import numpy as np

# Design problem (decision)
# 1. do we need a read_txtfile function to readfile into attribute?
# or we can directly read file in constructor
class Synthesizer():

    def __init__(self, TENT_str_list, beats_str_list):
        
        #[Todo]
        if isinstance(TENT_str_list, list) and isinstance(beats_str_list, list):
            self.raw_TENT_final_notes = TENT_str_list
            self.raw_beats = beats_str_list
            self.beat_duration = -1
            
    def clean_raw_data(self):
        self.raw_TENT_final_notes = None

    def generate_from_soloLa(self):
        pass
    
    def calculate_beat_duration(self, cal_mode="mode"):    
        
        # parse data input numpy array
        time = []
        for l in self.raw_beats:
            l_segment =l.replace('\n','').split(",")
            time.append(float(l_segment[1]))
        
        # prepare two nparary
        np_array = np.array(time)

        # larger = np.delete(np_array,0)
        # smaller = np.delete(np_array,np_array.size-1)
        raw_duration = np.delete(np_array,0) - np.delete(np_array,np_array.size-1)
        # print(raw_duration)
        
        if cal_mode == "mode":
            # mode number 
            distr =np.histogram(raw_duration,bins=10)
            # print(distr)
            max_index = np.argmax(distr[0])
            # print(distr[1][max_index])
            self.beat_duration = distr[1][max_index]
        
        elif cal_mode == "mean":
            # print(np.mean(raw_duration))
            self.beat_duration = np.mean(raw_duration)
    
    def calcalate_notes_duration(self):
        pass

    def calculate_default_picth_notation(self):
        pass

    def create_musicXML_basic_template(self):
         
        root_score_tag = ET.Element("score-partwise", version="3.1")
        root_score_tag.append(ET.Element("movement-title"))
        root_score_tag.append(ET.Element("identification"))
        root_score_tag.append(ET.Element("part-list"))
        root_score_tag.append(ET.Element("part"))
        
        # print(ET.tostring(root_score_tag, pretty_print=True))
        pass
# 
#   Utility function
# 

# PURPOSE: Read raw text file
# PARAMETERS: [file_path]
# RETURN: [string[]]
def read_raw_file(p):

    result_list = []
    # detect non-exist file path
    fp = Path(p)
    if not fp.is_file():
        print("Path:{}, Contnet: {}".format("Invalid",""))
    with open(p, 'r') as f:
        result_list = f.readlines()
    
    # show content
    # print("Path:{}, Contnet: {}".format(p,result_list))

    return result_list
    