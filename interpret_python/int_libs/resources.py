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
    TYPE = 208
    SYMBOL = 209
    ERROR = 666

class Opcode:
    identif = None
    def __init__(self, identif):
        self.identif = identif

class Operand:
    identif = None
    type = None
    data_type = None
    data = None
    defined = False
    
    def __ParseType(self):
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
        self.__ParseType()
    
    def ChangeDataType(self, data_type):
        self.data_type = data_type
        
    def ChangeData(self, data):
        self.data = data
        self.__ParseType()
        
    def IsSymbol(self):
        symbols = [Types.VAR, Types.INT, Types.BOOL, Types.STRING, Types.NIL]
        if self.type in symbols:
            return True
        return False
    def DefineVar(self):
        self.defined = True
    def IsDefined(self):
        if (self.type is Types.VAR and self.defined) or self.type is not Types.VAR:
            return True
        return False
    
class Symtable:
    data = None
    def __init__(self):
        self.data = []
    def AddChangeToken(self, identif, type, data_type, data):
        token = None
        for data_token in self.data:
            if data_token.identif == identif and data_token.type == type:
                token = data_token
        
        if token is None:
            token = Operand(identif, type, data_type, data)
            self.data.append(token)
        else:
            if data_type is not None:
                token.data_type = data_type
            if data is not None:
                token.data = data
            
        return token

    def FindToken(self, identif, type):
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
    def AddLabel(self, label, line):
        if label in self.labels:
            raise Exception(Errors.SEM)
        self.labels[label] = line
    def AddLine(self, line, order):
        if len(self.lines) > 0:
            if order in self.lines:
                raise Exception(Errors.XML_STRUCT)
        self.lines[order] = line



class Errors:
    XML_WF = 31
    XML_STRUCT = 32
    SEM = 52
    RUN_TYPES = 53
    RUN_VAR = 54
    RUN_NOTEX = 55
    RUN_VALMISS = 56
    RUN_OPVAL = 57
    RUN_STRING = 58   
    INTERNAL = 99
    messages = {
                XML_WF: "chybny XML format ve vstupnim souboru",
                XML_STRUCT: "neocekavana struktura XML",
                SEM: "chyba pri semantickych kontrolach vstupniho kodu v IPPcode23 (napr. pouziti nedefinovaneho navesti, redefinice promenne)",
                RUN_TYPES: "behova chyba interpretace – spatne typy operandu",
                RUN_VAR: "behova chyba interpretace – pristup k neexistujici promenne (ramec existuje)",
                RUN_NOTEX :"behova chyba interpretace – ramec neexistuje (napr. cteni z prazdneho zasobniku ramcu)",
                RUN_VALMISS :"behova chyba interpretace – chybejici hodnota (v promenne, na datovem zasobniku nebov zasobniku volani)",
                RUN_OPVAL :"behova chyba interpretace – spatna hodnota operandu (napr. deleni nulou, spatna navra-tova hodnota instrukce EXIT)",
                RUN_STRING :"behova chyba interpretace – chybna prace s retezcem"
    }
    
    def Exit(code, message = None, file = None):
        if file != None and file != sys.stdin:
            file.close()
        if message == None:
            if code != Errors.INTERNAL:
                message = Errors.messages[code]
            else:
                message = "vnitrni chyba interpretu"
        sys.stderr.write(message+"\n")
        exit(code)