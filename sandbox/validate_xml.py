from lxml import etree, objectify
from lxml.etree import XMLSyntaxError, fromstring
def xml_validator(some_xml_string, xsd_file='/path/to/my_schema_file.xsd'):
    try:
        schema = etree.XMLSchema(file=xsd_file)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(some_xml_string, parser)
        print ("YEAH!, my xml file has validated")
    except XMLSyntaxError:
        #handle exception here
        print ("Oh NO!, my xml file does not validate")
        pass

xml_path = '../reference/hello_world.xml'
xsd_path = './musicxml.xsd'

xml_file = open(xml_path, 'r')
xml_string = xml_file.read().encode('utf-8')
xml_file.close()
parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
xml_string = fromstring(xml_string, parser=parser)
xml_validator(xml_string, xsd_path)