#
# soubor:   scanner.py
# autor:    Michal Novák <xnovak3>  
# Tento modul slouží k načtení vstupu z XML souboru   
#

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
        return Types.ERROR # chyba při chybném typu

    # načtení a zpracování XML souboru
    @staticmethod
    def GetTokens(xml_file):
        order = 0

        # otevření XML souboru
        try:
            if xml_file != sys.stdin:
                xml_file = open(xml_file, "r")
        except:
            Errors.Exit(Errors.INTERNAL)
        
        code = Code() # inicializace kódu
        # získání struktury XML souboru
        try:
            tree = ET.parse(xml_file)
        except:
            Errors.Exit(Errors.XML_WF)
        
        # soubor je po získání struktury možné zavřít
        if xml_file != sys.stdin:
            xml_file.close()
        
        # získání kořene XML struktury
        root = tree.getroot()
        
        # ošetření XML formátu
        if 'language' not in root.attrib.keys():
            Errors.Exit(Errors.XML_STRUCT)
        if root.attrib['language'] != "IPPcode23" or root.tag != "program":
            Errors.Exit(Errors.XML_STRUCT)

        # získání dat z XML reprezentace
        for instruction in root:
            # ošetření XML formátu
            if instruction.tag != "instruction":
                Errors.Exit(Errors.XML_STRUCT)
            
            line = []
            
            # ošetření XML formátu
            if 'order' not in instruction.attrib.keys() or 'opcode' not in instruction.attrib.keys():
                Errors.Exit(Errors.XML_STRUCT)
            if not instruction.attrib['order'].isdigit():
                Errors.Exit(Errors.XML_STRUCT)
            
            order = int(instruction.attrib['order']) # pořadí instrukce
            token = Opcode(instruction.attrib['opcode'].upper()) # operační kó instrukce
            line.append(token) # přidání operačního k´du do řádku instrukce
            argsLine={} # argumnty pro instrukci
            
            # získání argumnetů instrukce
            for args in instruction:
                # ošetření XML formátu
                if re.match("^arg[1-3]$",args.tag) == None:
                    Errors.Exit(Errors.XML_STRUCT)
                if 'type' not in args.attrib.keys():
                    Errors.Exit(Errors.XML_STRUCT)
                
                type = Scanner.GetType(args.attrib['type']) # získání typu argumentu
                
                if type != Types.ERROR:
                    identif = args.text
                    if identif != None:
                        identif = identif.strip()
                    token = code.symtable.AddChangeToken(identif, type, None, None)
                    if token == None:
                        Errors.Exit(Errors.XML_STRUCT)
                    argsLine[args.tag] = token
                    
                    if 'opcode' not in instruction.attrib.keys():
                        Errors.Exit(Errors.XML_STRUCT)
                    if type == Types.LABEL and instruction.attrib['opcode'] == "LABEL":
                        if code.AddLabel(token, order) == False:
                            Errors.Exit(Errors.SEM)
                else:
                    print(args.attrib['type'], "::", Scanner.GetType(args.attrib['type']), order)
                    Errors.Exit(Errors.XML_STRUCT)
                    
            
            # seřazení argumentů a přiřazení na řádek instrukce
            argsLine = dict(sorted(argsLine.items()))
            for argKey in argsLine:
                if int(argKey[3]) !=  len(line):
                    Errors.Exit(Errors.XML_STRUCT)
                line.append(argsLine[argKey])
            if code.AddLine(line, order) == False:
                Errors.Exit(Errors.XML_STRUCT)
        
        return code
