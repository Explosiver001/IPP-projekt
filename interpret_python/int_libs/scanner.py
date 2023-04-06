import xml.etree.ElementTree as ET
import sys
from enum import Enum
from .shared import *
from array import array
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

class Token:
    identif = None
    type = None
    data_type = None
    data = None
    defined = False
    
    def __parseType(self):
        try:
            if self.type is Types.STRING or self.data_type is Types.STRING:
                self.data_type = Types.STRING
                if self.data is None:
                    self.data = ""
                while self.data.find("\\") >= 0:
                    index = self.data.find("\\")
                    subs = self.data[index+1]+self.data[index+2]+self.data[index+3]
                    self.data = self.data.replace('\\'+subs, chr(int(subs)))
            elif self.type is Types.INT or self.data_type is Types.INT:
                self.data_type = Types.INT
                if self.data.isdigit() == False and not (self.data[1:].isdigit() == True and self.data[0] == '-'):
                    raise BaseException
                self.data = int(self.data)
            elif self.type is Types.BOOL or self.data_type is Types.BOOL:
                self.data_type = Types.BOOL
                self.data = True if self.data.lower() == "true" else False
            elif self.type is Types.NIL:
                self.data_type = Types.NIL
                self.data = None
        except BaseException:
            Errors.Exit(Errors.XML_STRUCT)
        except:
            Errors.Exit(Errors.RUN_TYPES)
            
    def __init__(self, identif, type, data_type, data):
        self.identif = identif
        self.type = type
        self.data_type = data_type
        self.data = data
        if type is Types.STRING or type is Types.BOOL or type is Types.INT or type is Types.NIL:
            self.data = identif
        self.__parseType()
    
    def changeDataType(self, data_type):
        self.data_type = data_type
        
    def changeData(self, data):
        self.data = data
        self.__parseType()
        
    def isSymbol(self):
        symbols = [Types.VAR, Types.INT, Types.BOOL, Types.STRING, Types.NIL]
        if self.type in symbols:
            return True
        return False
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
            if data_token.identif == identif and data_token.type == type:
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

    def findToken(self, identif, type):
        for token in self.data:
            if token.identif == identif and token.type == type:
                return token
        return None
    
    def print(self):
        print("Symtable data:")
        for token in self.data:
            print("{",token.identif, ";", token.type,";", token.data, "}")

class Code:
    symtable = None
    lines = dict()
    labels = None
    
    def __init__(self):
        self.lines = dict()
        self.labels = {}
        self.symtable = Symtable()
    def addLabel(self, label, line):
        if label in self.labels:
            raise Exception(Errors.SEM)
        self.labels[label] = line
    def addLine(self, line, order):
        if len(self.lines) > 0:
            if order in self.lines:
                raise Exception(Errors.XML_STRUCT)
        self.lines[order] = line

    
def GetType(name):
    arr = {"var":Types.VAR, "int":Types.INT, "bool":Types.BOOL, "string":Types.STRING, "nil":Types.NIL, "label":Types.LABEL, "type":Types.TYPE}
    if name in arr:
        return arr[name]
    return Types.ERROR

def get_tokens(xml_file):
    order = 0
    
    try:
        if xml_file != sys.stdin:
            xml_file = open(xml_file, "r")
    except:
        Errors.Exit(Errors.INTERNAL)
    
    code = Code()
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        if root.attrib['language'] != "IPPcode23" or root.tag != "program":
            raise Exception(Errors.XML_STRUCT)
        
        for instruction in root:
            if instruction.tag != "instruction":
                raise Exception(Errors.XML_STRUCT)
            line = []
            order = int(instruction.attrib['order'])
            token = Token(instruction.attrib['opcode'], Types.OPCODE, None, None)
            line.append(token)
            argsLine={}
            
            for args in instruction:
                if re.match("^arg[1-3]$",args.tag) == None:
                    raise Exception(Errors.XML_STRUCT)
                type = GetType(args.attrib['type'])
                if type != Types.ERROR:
                    token = code.symtable.add_change_token(args.text, type, None, None)
                    argsLine[args.tag] = token
                    
                    if type == Types.LABEL and instruction.attrib['opcode'] == "LABEL":
                        code.addLabel(token, order)
                else:
                    print(args.attrib['type'].ljust(7), "::", GetType(args.attrib['type']))
            
            argsLine = dict(sorted(argsLine.items()))
            
            for argKey in argsLine:
                line.append(argsLine[argKey])
            code.addLine(line, order)
    except ET.ParseError:
        Errors.Exit(Errors.XML_WF)
    
    except KeyError:
        Errors.Exit(Errors.XML_STRUCT)
        
    except ValueError:
        Errors.Exit(Errors.XML_STRUCT)
    
    except Exception as Error:
        Errors.Exit(int(Error.args[0]))
            

    if xml_file != sys.stdin:
        xml_file.close()


    return code