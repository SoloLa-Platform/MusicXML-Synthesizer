from MusicXMLSynthesizer.Synthesizer import Synthesizer
from MusicXMLSynthesizer.utils import parse_notes_meta_to_list, write_file
# input solola_list, downbeat_list, beat_list, xsd_path(default: in package)
# flag --validate -o(output absolute file_path: default behavior create )
# output 

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, 
        description=
    """
===================================================================
Script for synthesize solola output with downbeat and beat into musicXML.
===================================================================
    """)
    parser.add_argument('-s', '--solola_path', type=str, help="absolute path of solola output file")
    parser.add_argument('-db', '--downbeat_path', type=str, help="absolute path of downbeat output file")
    parser.add_argument('-b', '--beat_path', type=str, help="absolute path of beat output file")
    parser.add_argument('-o', '--output_path', type=str, help="absolute path of synthesize output file", default="./outputs/output.musicxml")
    parser.add_argument('-d', '---xsd_path', type=str, help="absolute path of dtd/xsd output file", default="./musicxml-3.1-dtd-xsd/schema/musicxml.xsd")
    parser.add_argument('-x', '--execute_validation', type=bool, help="validate output with musicXML DTD/XSD after generated")
    
    return parser.parse_args()

def synthesize(args):
    # print(args)

    # Read file
    solola_list = parse_notes_meta_to_list(
        args.solola_path)
    beats_list = parse_notes_meta_to_list(
        args.beat_path)
    downbeats_list = parse_notes_meta_to_list(
        args.downbeat_path)

    # setup
    synthesizer = Synthesizer(args.xsd_path)
    synthesizer.save(solola_list, downbeats_list, beats_list)

    # synthesize musicXML
    xml = synthesizer.execute()

    # create folder and write file to file system
    write_file(args.output_path, xml)

if __name__ == '__main__':
    args = parse_args()
    synthesize(args)
