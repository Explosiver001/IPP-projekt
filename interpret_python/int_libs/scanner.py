import xml.etree.ElementTree as ET
import sys
from enum import Enum
import re

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

#def parse_string(IPPstring):
#    if IPPstring is None:
#        return ""
#    while IPPstring.find("\\") >= 0:
#        index = IPPstring.find("\\")
#        subs = IPPstring[index+1]+IPPstring[index+2]+IPPstring[index+3]
#        IPPstring = IPPstring.replace('\\'+subs, chr(int(subs)))
#    return IPPstring


class Token:
    identif = None
    type = None
    data_type = None
    data = None
    
    
    def __parseType(self):
        if self.type is None:
            return
        if self.type is Types.STRING:
            self.data = self.identif
            if self.data is None:
                self.data = ""
            while self.data.find("\\") >= 0:
                index = self.data.find("\\")
                subs = self.data[index+1]+self.data[index+2]+self.data[index+3]
                self.data = self.data.replace('\\'+subs, chr(int(subs)))
        elif self.type is Types.INT:
            self.data = self.identif
            self.data = int(self.identif)
        elif self.type is Types.BOOL:
            self.data = self.identif
            self.data = True if self.data == "true" else False
        elif self.type is Types.NIL:
            self.data = self.identif
            self.data = None
            
    def __init__(self, identif, type, data_type, data):
        self.identif = identif
        self.type = type
        self.data_type = data_type
        self.data = data
        self.__parseType()
    
    def changeDataType(self, data_type):
        self.data_type = data_type
        
    def changeData(self, data):
        self.data = data
        
    
        
class Code:
    lines = None
    labels = None
    def __init__(self):
        self.lines = []
        self.labels = {}
    def addLabel(self, label, line):
        self.labels[label] = line
    def addLine(self, line):
        self.lines.append(line)
    
def GetType(name):
    arr = {"var":Types.VAR, "bool":Types.BOOL, "string":Types.STRING, "nil":Types.NIL, "label":Types.LABEL}
    if name in arr:
        return arr[name]
    return Types.ERROR

def get_tokens(xml_file):
    order = 0
    
    if xml_file != sys.stdin:
        xml_file = open(xml_file, "r")
    
    code = Code()
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for instruction in root:
            line = []
            order = int(instruction.attrib['order'])
            token = Token(instruction.attrib['opcode'], Types.OPCODE, None, None)
            line.append(token)
            for args in instruction:
                type = GetType(args.attrib['type'])
                if type != Types.ERROR:
                    token = Token(args.text, type, None, None)
                    line.append(token)
                    if type == Types.LABEL and instruction.attrib['opcode'] == "LABEL":
                        code.addLabel(args.text, order)
                    
                else:
                    print(args.attrib['type'].ljust(7), "::", GetType(args.attrib['type']))
            code.addLine(line)
    except:
        print(Types.ERROR)

    print(code.labels)
    #for line in code.lines:
    #    for token in line:
    #        print(token.data, end="  ")
    #    print()

    
    return code