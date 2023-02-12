import xml.etree.ElementTree as ET
import sys

class Token:
    def __init__(self, identif, type, data_type, data):
        self.identif = identif
        self.type = type
        self.data_type = data_type
        self.data = data
    
    def changeDataType(self, data_type):
        self.data_type = data_type
        
    def changeData(self, data):
        self.data = data
        
class Code:
    def __init__(self):
        self.lines = []
        self.labels = []
    def addLabel(self, label, line):
        self.labels.insert(label,line)
    def addLine(self, line):
        self.lines.append(line)
    
    

def get_tokens(xml_file):
    linenum = 1
    
    if xml_file != sys.stdin:
        xml_file = open(xml_file, "r")
        
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for instruction in root:
        #print(instruction.tag, instruction.attrib)
        for args in instruction:
            #print(args.tag, args.attrib, args.text)
            print(args.attrib['type'].ljust(7), "::", args.text)
        
    

    
    return