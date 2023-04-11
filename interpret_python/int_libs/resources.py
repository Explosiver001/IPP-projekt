#
# soubor:   resources.py
# autor:    Michal Novák <xnovak3>  
# Modul obsahuje prostředky sdílené se všemi moduly. Jsou zde třídy pro základní jednotky interpretu a chybové ukončení.   
#

import sys
from enum import Enum

source_file = sys.stdin
input_file = None

# vnitřní reprezentace typů
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

# třída pro operační kódy
class Opcode:
    identif = None
    def __init__(self, identif):
        self.identif = identif

# třída pro agrumenty (operandy)
class Operand:
    identif = None      # název
    type = None         # typ vnější
    data_type = None    # typ vnitřní 
    data = None         # data argumetu
    defined = False     # je li argument definován
    
    # zpracování dat na patřičný datový typ
    def ParseType(self):
        try:
            if self.type is Types.STRING or self.data_type is Types.STRING:
                self.data_type = Types.STRING
                if self.data is None:
                    self.data = ""
                # náhrada escape-sekvencí za znaky
                while self.data.find("\\") >= 0:
                    index = self.data.find("\\")
                    if index+3 >= len(self.data):
                        break
                    subs = self.data[index+1]+self.data[index+2]+self.data[index+3]
                    self.data = self.data.replace('\\'+subs, chr(int(subs)))
            elif self.type is Types.INT or self.data_type is Types.INT:
                self.data_type = Types.INT
                if self.data.isdigit() == False and not (self.data[1:].isdigit() == True and self.data[0] == '-'):
                    return False
                self.data = int(self.data)
            elif self.type is Types.BOOL or self.data_type is Types.BOOL:
                self.data_type = Types.BOOL
                self.data = True if self.data.lower() == "true" else False
            elif self.type is Types.NIL:
                self.data_type = Types.NIL
                self.data = None
            return True
        except:
            return(Errors.RUN_TYPES)
    
    # inicializace
    def __init__(self, identif, type, data_type, data):
        self.identif = identif
        self.type = type
        self.data_type = data_type
        self.data = data
        if type is Types.STRING or type is Types.BOOL or type is Types.INT or type is Types.NIL:
            self.data = identif

    # změna datového typu
    def ChangeDataType(self, data_type):
        self.data_type = data_type

    # změna dat
    def ChangeData(self, data):
        self.data = data
        return self.ParseType()

    # ověření, že operand je symbol
    def IsSymbol(self):
        symbols = [Types.VAR, Types.INT, Types.BOOL, Types.STRING, Types.NIL]
        if self.type in symbols:
            return True
        return False

    # definice proměnné
    def DefineVar(self):
        self.defined = True

    # ověření, že je proměnná definovaná
    def IsDefined(self):
        if (self.type is Types.VAR and self.defined) or self.type is not Types.VAR:
            return True
        return False

# třída tabulky symbolů
class Symtable:
    data = None # seznam symbolů
    def __init__(self):
        self.data = []
    
    # přidání tokenu do tabulky symbolů
    def AddChangeToken(self, identif, type, data_type, data):
        token = None
        # token existuje, nevytváří se nový token
        for data_token in self.data:
            if data_token.identif == identif and data_token.type == type:
                token = data_token
        
        # token neexistuje, vytváří se nový token
        if token is None:
            token = Operand(identif, type, data_type, data)
            if token.ParseType() == False:
                return None
            self.data.append(token)
        else:
            if data_type is not None:
                token.data_type = data_type
            if data is not None:
                token.data = data
        
        # nový/nalezený token
        return token

    # vyhledá token v tabulce symbolů
    def FindToken(self, identif, type):
        for token in self.data:
            if token.identif == identif and token.type == type:
                return token
        return None
    
    # vytiskne tabulku symbolů (debug)
    def print(self):
        print("Symtable data:")
        for token in self.data:
            print("{",token.identif, ";", token.type,";", token.data, "}")

# třída pro uchování kódu
class Code:
    symtable = None # tabulka symbolů
    lines = dict() # jednotlivé řádky instrukcí
    labels = None # seznam návěští
    
    def __init__(self):
        self.lines = dict()
        self.labels = {}
        self.symtable = Symtable()
    
    # přidání návěští do seznamu
    def AddLabel(self, label, line):
        if label in self.labels:
            return False
        self.labels[label] = line
        return True

    # přidání řádku s instrukcí
    def AddLine(self, line, order):
        if order < 1:
            return False
        if len(self.lines) > 0:
            if order in self.lines:
                return False
        self.lines[order] = line
        return True


# chyby a chybové ukončení
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
    
    # předem definované hlášky
    messages = {
                XML_WF: "chybny XML format ve vstupnim souboru",
                XML_STRUCT: "neocekavana struktura XML",
                SEM: "chyba pri semantickych kontrolach vstupniho kodu v IPPcode23 (napr. pouziti nedefinovaneho navesti, redefinice promenne)",
                RUN_TYPES: "behova chyba interpretace – spatne typy operandu",
                RUN_VAR: "behova chyba interpretace – pristup k neexistujici promenne (ramec existuje)",
                RUN_NOTEX :"behova chyba interpretace – ramec neexistuje (napr. cteni z prazdneho zasobniku ramcu)",
                RUN_VALMISS :"behova chyba interpretace – chybejici hodnota (v promenne, na datovem zasobniku nebov zasobniku volani)",
                RUN_OPVAL :"behova chyba interpretace – spatna hodnota operandu (napr. deleni nulou, spatna navra-tova hodnota instrukce EXIT)",
                RUN_STRING :"behova chyba interpretace – chybna prace s retezcem",
                INTERNAL: "vnitrni chyba interpretu"
    }
    
    # ukončí interpret s chybovým kódem a hláškou
    def Exit(code, message = None):
        if source_file != None and source_file != sys.stdin:
            source_file.close()
        if input_file != None and input_file != sys.stdin:
            input_file.close()
        if message == None:
            message = Errors.messages[code]
        sys.stderr.write(message+"\n")
        exit(code)