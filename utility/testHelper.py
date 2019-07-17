from pathlib import Path
from lxml import etree as ET


def read_musicxml(path):
    file_path = Path(path)
    if not file_path.is_file():
        print("Path:{}, Contnet: {}".format("Invalid", ""))
    else:
        tree = ET.parse(str(file_path))
        return ET.tostring(tree, xml_declaration=True,
                           encoding="UTF-8",doctype="""<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">""").decode("UTF-8")


