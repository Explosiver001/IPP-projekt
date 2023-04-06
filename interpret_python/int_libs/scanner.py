import xml.etree.ElementTree as ET
import sys
from .resources import *
import re


class XMLStructException(Exception):
    pass
class XMLWellFormed(Exception):
    pass

# Třída pro získání kódu ze vstupu
class Scanner:
    # převede typ na vnitřní reprezentaci
    def GetType(name):
        arr = {"var":Types.VAR, "int":Types.INT, "bool":Types.BOOL, "string":Types.STRING, "nil":Types.NIL, "label":Types.LABEL, "type":Types.TYPE}
        if name in arr:
            return arr[name]
        return Types.ERROR

    # načtení a zpracování XML souboru
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
            root = tree.getroot()
            
            if root.attrib['language'] != "IPPcode23" or root.tag != "program":
                raise Exception(Errors.XML_STRUCT)
            
            for instruction in root:
                if instruction.tag != "instruction":
                    raise Exception(Errors.XML_STRUCT)
                line = []
                order = int(instruction.attrib['order'])
                token = Opcode(instruction.attrib['opcode'])
                line.append(token)
                argsLine={}
                
                for args in instruction:
                    if re.match("^arg[1-3]$",args.tag) == None:
                        raise Exception(Errors.XML_STRUCT)
                    type = Scanner.GetType(args.attrib['type'])
                    if type != Types.ERROR:
                        token = code.symtable.AddChangeToken(args.text, type, None, None)
                        argsLine[args.tag] = token
                        
                        if type == Types.LABEL and instruction.attrib['opcode'] == "LABEL":
                            code.AddLabel(token, order)
                    else:
                        print(args.attrib['type'].ljust(7), "::", Scanner.GetType(args.attrib['type']))
                
                argsLine = dict(sorted(argsLine.items()))
                
                for argKey in argsLine:
                    line.append(argsLine[argKey])
                code.AddLine(line, order)
        except ET.ParseError:
            Errors.Exit(Errors.XML_WF, file=xml_file)
        
        except KeyError:
            Errors.Exit(Errors.XML_STRUCT, file=xml_file)
            
        except ValueError:
            Errors.Exit(Errors.XML_STRUCT, file=xml_file)
        
        except Exception as Error:
            Errors.Exit(int(Error.args[0]), file=xml_file)
                
        if xml_file != sys.stdin:
            xml_file.close()
            
        return code