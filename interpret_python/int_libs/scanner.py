import xml.etree.ElementTree as ET
import sys
from enum import Enum

class Types(Enum):
    OPCODE = 200
    INT = 201
    STRING = 202
    BOOL = 203
    NIL = 204
    VAR = 205
    LABEL = 206
    NONE = 207
    ERROR = 208
    
    


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
    
def GetType(name):
    arr = {"var":Types.VAR, "bool":Types.BOOL, "string":Types.STRING, "nil":Types.NIL, "label":Types.LABEL}
    if name in arr:
        return arr[name]
    return Types.ERROR

def get_tokens(xml_file):
    linenum = 1
    
    if xml_file != sys.stdin:
        xml_file = open(xml_file, "r")
        
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for instruction in root:
        line = []
        token = Token(instruction.attrib['opcode'], Types.OPCODE, None, None)
        line.append(token)
        #print(instruction.attrib['opcode'])
        for args in instruction:
            #print(args.tag, args.attrib, args.text)
            print(args.attrib['type'].ljust(7), "::", GetType(args.attrib['type']))

            
        
    

    
    return