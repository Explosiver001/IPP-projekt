import xml.etree.ElementTree as ET
import sys
from .resources import *
import re

# Třída pro získání kódu ze vstupu
class Scanner:
    # převede typ na vnitřní reprezentaci
    @staticmethod
    def GetType(name):
        arr = {"var":Types.VAR, "int":Types.INT, "bool":Types.BOOL, "string":Types.STRING, "nil":Types.NIL, "label":Types.LABEL, "type":Types.TYPE}
        if name in arr:
            return arr[name]
        return Types.ERROR

    # načtení a zpracování XML souboru
    @staticmethod
    def GetTokens(xml_file):
        order = 0

        try:
            if xml_file != sys.stdin:
                xml_file = open(xml_file, "r")
        except:
            Errors.Exit(Errors.INTERNAL)
        
        code = Code()
        try:
            tree = ET.parse(xml_file)
        except:
            Errors.Exit(Errors.XML_WF, file=xml_file)
        root = tree.getroot()
        
        
        if 'language' not in root.attrib.keys():
            Errors.Exit(Errors.XML_STRUCT, file=xml_file)
        if root.attrib['language'] != "IPPcode23" or root.tag != "program":
            Errors.Exit(Errors.XML_STRUCT, file=xml_file)

            
        
        for instruction in root:
            if instruction.tag != "instruction":
                Errors.Exit(Errors.XML_STRUCT, file=xml_file)
            line = []
            if 'order' not in instruction.attrib.keys() or 'opcode' not in instruction.attrib.keys():
                Errors.Exit(Errors.XML_STRUCT, file=xml_file)
            if not instruction.attrib['order'].isdigit():
                Errors.Exit(Errors.XML_STRUCT, file=xml_file)
            order = int(instruction.attrib['order'])
            token = Opcode(instruction.attrib['opcode'].upper())
            line.append(token)
            argsLine={}
            
            for args in instruction:
                if re.match("^arg[1-3]$",args.tag) == None:
                    Errors.Exit(Errors.XML_STRUCT, file=xml_file)
                
                if 'type' not in args.attrib.keys():
                    Errors.Exit(Errors.XML_STRUCT, file=xml_file)
                type = Scanner.GetType(args.attrib['type'])
                if type != Types.ERROR:
                    token = code.symtable.AddChangeToken(args.text, type, None, None)
                    if token == None:
                        Errors.Exit(Errors.XML_STRUCT, file=xml_file)
                    argsLine[args.tag] = token
                    
                    if 'opcode' not in instruction.attrib.keys():
                        Errors.Exit(Errors.XML_STRUCT, file=xml_file)
                    if type == Types.LABEL and instruction.attrib['opcode'] == "LABEL":
                        if code.AddLabel(token, order) == False:
                            Errors.Exit(Errors.SEM, file=xml_file)
                else:
                    print(args.attrib['type'].ljust(7), "::", Scanner.GetType(args.attrib['type']))
            
            argsLine = dict(sorted(argsLine.items()))
            
            for argKey in argsLine:
                line.append(argsLine[argKey])
            if code.AddLine(line, order) == False:
                Errors.Exit(Errors.XML_STRUCT, file=xml_file)
        
        if xml_file != sys.stdin:
            xml_file.close()
            
        return code