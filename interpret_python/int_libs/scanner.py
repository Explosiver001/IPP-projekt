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
    TYPE = 208
    SYMBOL = 209
    ERROR = 666

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
    defined = False
    
    def __parseType(self):
        if self.type is None:
            return
        if self.type is Types.STRING:
            self.data_type = Types.STRING
            self.data = self.identif
            if self.data is None:
                self.data = ""
            while self.data.find("\\") >= 0:
                index = self.data.find("\\")
                subs = self.data[index+1]+self.data[index+2]+self.data[index+3]
                self.data = self.data.replace('\\'+subs, chr(int(subs)))
        elif self.type is Types.INT:
            self.data_type = Types.INT
            self.data = self.identif
            self.data = int(self.identif)
        elif self.type is Types.BOOL:
            self.data_type = Types.BOOL
            self.data = self.identif
            self.data = True if self.data == "true" else False
        elif self.type is Types.NIL:
            self.data_type = Types.NIL
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
        
    def isSymbol(self):
        symbols = [Types.VAR, Types.INT, Types.BOOL, Types.STRING, Types.NIL]
        if self.type in symbols:
            return True
        return False
    def isVar(self):
        return self.type is Types.VAR
    def isLabel(self):
        return self.type is Types.LABEL
    def isString(self):
        return self.type is Types.STRING
    def isInt(self):
        return self.type is Types.INT
    def isBool(self):
        return self.type is Types.BOOL
    def isNil(self):
        return self.type is Types.NIL
    def isType(self):
        return self.type is Types.TYPE
    def defineVar(self):
        self.defined = True
    def isDefined(self):
        if (self.type is Types.VAR and self.defined) or self.type is not Types.VAR:
            return True
        return False
    
class Symtable:
    data = None
    def __init__(self):
        self.data = []
    def add_change_token(self, identif, type, data_type, data):
        token = None
        for data_token in self.data:
            if data_token.identif == identif:
                token = data_token
        
        if token is None:
            token = Token(identif, type, data_type, data)
            self.data.append(token)
        else:
            if data_type is not None:
                token.data_type = data_type
            if data is not None:
                token.data = data
            
        return token
    
    def print(self):
        print("Symtable data:")
        for token in self.data:
            print("{",token.identif, ";", token.type,";", token.data, "}")

class Code:
    symtable = None
    lines = None
    labels = None
    
    def __init__(self):
        self.lines = []
        self.labels = {}
        self.symtable = Symtable()
    def addLabel(self, label, line):
        self.labels[label] = line
    def addLine(self, line):
        self.lines.append(line)
    
def GetType(name):
    arr = {"var":Types.VAR, "bool":Types.BOOL, "string":Types.STRING, "nil":Types.NIL, "label":Types.LABEL, "type":Types.TYPE}
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
                    token = code.symtable.add_change_token(args.text, type, None, None)
                    line.append(token)
                    if type == Types.LABEL and instruction.attrib['opcode'] == "LABEL":
                        code.addLabel(token, order)
                    
                else:
                    print(args.attrib['type'].ljust(7), "::", GetType(args.attrib['type']))
            code.addLine(line)
    except:
        print(Types.ERROR)



    
    return code