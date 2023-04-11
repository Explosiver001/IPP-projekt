#
# soubor:   execution.py
# autor:    Michal Novák <xnovak3>  
# Tento modul zajišťuje vykonávání jednotlivých instrukcí 
#

from .scanner import *
from .resources import *
import fileinput

class Runner:
    def __init__(self, input):
        self.input = input # vstupní soubor
        self.PC_stack = [] # zásobník pozice pro návrat z funkcí
        self.data_stack = [] # datový zásobník
        self.local_frame = [] # pole lokální rámex
        self.local_frame_backup = [] # pole záloh lokálních rámců
        self.temporal_frame = [] # dočasný rámec
        self.createFrame = False # informace o vytvořní lokálního rámce
        self.instructionsPreformed = 0 # počet vykonaných instrukcí
        # uložení uživatelských vstupů ze souboru
        if self.input != None: 
            self.inputLines = [] # uživatelské vstupy
            for line in self.input:
                self.inputLines.append(line.rstrip("\n"))
            self.inputLines.reverse() # otočení pole vstupů pro lepší přístup

    # načtení uživatelského vstupu
    def ReadInput(self):
        if self.input == None: # čtení z stdin
            str = input()
            return str
        else: # načítání z uložených vstupů (čtení ze souboru)
            if len(self.inputLines) > 0:
                str = self.inputLines.pop()
            else: # neodstatek vstupů (== EOF pro stdin)
                raise EOFError
            return str

    # vrátí lokální rámce
    def GetLocalFrames(self):
        return self.local_frame
    
    # vrátí dočasný rámec
    def GetTemporalFrame(self):
        return self.temporal_frame, self.createFrame

    # vykonání instrukce
    # instruction - aktuálná řádek (instrukce), který se má vykonat
    # code - celý kód uložený ve vnitřní reprezentaci
    # line - číslo aktuálního řádku
    
    # návratové hodnoty - None = bez skoku, číslo = skok (číslo udává řádek)
    def ExecuteInstruction(self, instruction, code, line):
        opcode = instruction[0] # operaní kód
        
        #získání argumentů z instrukce
        arg1 = None # argument 1
        arg2 = None # argument 2
        arg3 = None # argument 3
        if len(instruction) >= 4:
            arg3 = instruction[3]
        if len(instruction) >= 3:
            arg2 = instruction[2]
        if len(instruction) >= 2:
            arg1 = instruction[1]
        
        self.instructionsPreformed += 1 # zvýšení počítadla vykonaných instrukcí
        
        # jednotlivé operační kódy a vykonání instrukcí
        match opcode.identif:
            case "MOVE":
                arg1.data = arg2.data
                arg1.data_type = arg2.data_type

            case "CREATEFRAME":
                self.createFrame = True
                for var in self.temporal_frame:
                    var.defined = False
                self.temporal_frame = []

            case "PUSHFRAME":
                if self.createFrame == False: # nebyl vytvořen rámec
                    Errors.Exit(Errors.RUN_NOTEX)
                self.SaveLocalFrameData() # uložení dat lokálního rámce
                if len (self.local_frame) > 0:
                    for var in self.local_frame[len(self.local_frame)-1]:
                        var.data = None
                        var.defined = False
                self.local_frame.append(self.changeFrame(self.temporal_frame, code.symtable, "temporal")) 
                self.createFrame = False

            case "POPFRAME":
                if(len(self.local_frame) <= 0): # rámce neexistují
                    Errors.Exit(Errors.RUN_NOTEX)
                self.temporal_frame = self.changeFrame(self.local_frame.pop(), code.symtable, "local") 
                self.RestoreLocalFrameData() # obnova původních dat rámce
                self.createFrame = True

            case "DEFVAR":
                arg1.DefineVar()
                if str.find(arg1.identif, "LF@") != -1:
                    self.local_frame[len(self.local_frame)-1].append(arg1)
                elif str.find(arg1.identif, "TF@") != -1:
                    self.temporal_frame.append(arg1)

            case "CALL":
                if arg1 not in code.labels:
                    Errors.Exit(Errors.SEM)
                self.PC_stack.append(line) # uložení hodnoty pro zpětný skok
                return code.labels[arg1] # nová hodnota pro programový čítač

            case "RETURN":          
                if len(self.PC_stack) > 0:
                    ret = self.PC_stack.pop() # vyjmutí hodnoty pro zpětný skok
                    return ret + 1 
                else:
                    Errors.Exit(Errors.RUN_VALMISS)

            case "PUSHS":
                self.data_stack.append([arg1.data, arg1.data_type])

            case "POPS":
                if len(self.data_stack) != 0:
                    data = self.data_stack.pop()
                    arg1.data_type = data[1]
                    arg1.data = data[0]
                else:
                    Errors.Exit(Errors.RUN_VALMISS)

            case "ADD":
                arg1.data = arg2.data + arg3.data
                arg1.data_type = Types.INT

            case "SUB":
                arg1.data = arg2.data - arg3.data
                arg1.data_type = Types.INT

            case "MUL":
                arg1.data = arg2.data * arg3.data
                arg1.data_type = Types.INT

            case "IDIV":
                if arg3.data != 0:
                    arg1.data = arg2.data // arg3.data
                    arg1.data_type = Types.INT
                else:
                    Errors.Exit(Errors.RUN_OPVAL)

            case "LT":
                arg1.data_type = Types.BOOL
                arg1.data = (arg2.data < arg3.data)

            case "GT":
                arg1.data_type = Types.BOOL
                arg1.data = (arg2.data > arg3.data)

            case "EQ":
                if arg2.data_type == arg3.data_type:
                    arg1.data_type = Types.BOOL
                    arg1.data = (arg2.data == arg3.data)
                else: #1 z argumentů je NIL
                    arg1.data_type = Types.BOOL
                    arg1.data = False

            case "AND":
                arg1.data = arg2.data and arg3.data
                arg1.data_type = Types.BOOL

            case "OR":
                arg1.data = arg2.data or arg3.data
                arg1.data_type = Types.BOOL

            case "NOT":
                arg1.data = not arg2.data
                arg1.data_type = Types.BOOL

            case "INT2CHAR":
                arg1.data_type = Types.STRING
                if arg2.data >= 0 and arg2.data <= 0x10ffff: # kontrola rozsahu
                    arg1.data = chr(arg2.data)  
                else:
                    Errors.Exit(Errors.RUN_STRING)

            case "STRI2INT":
                if len(arg2.data) <= arg3.data or arg3.data < 0: # kontrola rozsahu
                    Errors.Exit(Errors.RUN_STRING)
                else:
                    arg1.data = ord(arg2.data[arg3.data])
                    arg1.data_type = Types.INT

            case "READ":
                try:
                    data = self.ReadInput()
                    arg1.ChangeDataType(Scanner.GetType(arg2.identif))
                    if arg1.ChangeData(data) == False:
                        raise EOFError
                except EOFError: # není dostatek uživatelských vstupů
                    arg1.data = ""
                    arg1.data_type = Types.NIL

            case "WRITE":
                if arg1.data_type is Types.NIL or arg1.data is None:
                    print("",end="")
                elif arg1.data_type is Types.BOOL:
                    if arg1.data is True:
                        print("true", end="")
                    else:
                        print("false", end="")
                else:
                    print(arg1.data, end="")

            case "CONCAT":
                arg1.data_type = Types.STRING
                arg1.data = arg2.data + arg3.data

            case "STRLEN":
                arg1.data_type = Types.INT
                arg1.data = len(arg2.data)

            case "GETCHAR":
                arg1.data_type = Types.STRING
                if len(arg2.data) > arg3.data and arg3.data >= 0:
                    arg1.data = arg2.data[arg3.data]
                else:
                    Errors.Exit(Errors.RUN_STRING)

            case "SETCHAR":
                if arg1.data_type != Types.STRING:
                    Errors.Exit(Errors.RUN_TYPES)
                if arg3.data == "":
                    Errors.Exit(Errors.RUN_STRING)
                if len(arg1.data) > arg2.data and arg2.data >= 0:
                    string = arg1.data
                    arg1.data = string[0:arg2.data] + arg3.data[0] + string[arg2.data+1:]    
                else:
                    Errors.Exit(Errors.RUN_STRING)

            case "TYPE":
                type = arg2.data_type
                arg1.data_type = Types.STRING
                match type:
                    case Types.INT:
                        arg1.data = "int"
                    case Types.STRING:
                        arg1.data = "string"
                    case Types.BOOL:
                        arg1.data = "bool"
                    case Types.NIL:
                        arg1.data = "nil"
                    case _:
                        arg1.data = ""

            case "LABEL":
                return None
            
            case "JUMP":
                if arg1 not in code.labels:
                    Errors.Exit(Errors.SEM)
                return code.labels[arg1]
            
            case "JUMPIFEQ":
                if arg1 not in code.labels:
                    Errors.Exit(Errors.SEM)
                if arg2.data_type is arg3.data_type:
                    if arg3.data == arg2.data: 
                        return code.labels[arg1]
                elif arg2.data_type is Types.NIL or arg3.data_type is Types.NIL:
                    if arg3.data == arg2.data: 
                        return code.labels[arg1]
                else:
                    Errors.Exit(Errors.RUN_TYPES)

            case "JUMPIFNEQ":
                if arg1 not in code.labels:
                    Errors.Exit(Errors.SEM)
                if arg2.data_type is arg3.data_type:
                    if arg3.data != arg2.data: 
                        return code.labels[arg1]
                elif arg2.data_type is Types.NIL or arg3.data_type is Types.NIL:
                    if arg3.data != arg2.data: 
                        return code.labels[arg1]
                else:
                    Errors.Exit(Errors.RUN_TYPES)

            case "EXIT":
                if arg1.data >= 0 and arg1.data <= 49:
                    exit(arg1.data)
                else:
                    Errors.Exit(Errors.RUN_OPVAL)

            case "DPRINT":
                if arg1.data_type is Types.NIL or arg1.data is None:
                    sys.stderr.write("")
                elif arg1.data_type is Types.BOOL:
                    if arg1.data is True:
                        sys.stderr.write("true")
                    else:
                        sys.stderr.write("false")
                else:
                    sys.stderr.write(arg1.data)

            case "BREAK":
                sys.stderr.write("Pocet vykonanych instrukci: " + self.instructionsPreformed + "\nPozice v kodu:\n\tORDER: " + line + "\n\tOPCODE: " + opcode)
                sys.stderr.write("LOCAL FRAME:")
                for token in self.local_frame[len(self.local_frame)-1]:
                    sys.stderr.write("\t" + token.identif + "\t" + token.data + "\t" + token.data_type)
                if self.createFrame:
                    for token in self.temporal_frame:
                        sys.stderr.write("\t" + token.identif + "\t" + token.data + "\t" + token.data_type)


            # Instrukce rozšíření STACK
            case "CLEARS":
                self.data_stack = []

            case "ADDS":
                symb1, symb2 = self.__stack_get2ints()
                self.data_stack.append([symb1 + symb2, Types.INT])

            case "SUBS":
                symb1, symb2 = self.__stack_get2ints()
                self.data_stack.append([symb1 - symb2, Types.INT])

            case "MULS":
                symb1, symb2 = self.__stack_get2ints()
                self.data_stack.append([symb1 * symb2, Types.INT])
                
            case "IDIVS":
                symb1, symb2 = self.__stack_get2ints()
                if symb2 == 0:
                    Errors.Exit(Errors.RUN_OPVAL)
                self.data_stack.append([symb1 // symb2, Types.INT])

            case "EQS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 == type2:
                    if symb1 == symb2: 
                        self.data_stack.append([True, Types.BOOL])
                    else:
                        self.data_stack.append([False, Types.BOOL])
                elif type1 == Types.NIL or type2 == Types.NIL:
                    self.data_stack.append([False, Types.BOOL])
                else:
                    Errors.Exit(Errors.RUN_TYPES)

            case "LTS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 == Types.NIL or type2 == Types.NIL:
                    Errors.Exit(Errors.RUN_TYPES)
                if type1 == type2:
                    if symb1 < symb2: 
                        self.data_stack.append([True, Types.BOOL])
                    else:
                        self.data_stack.append([False, Types.BOOL])
                else:
                    Errors.Exit(Errors.RUN_TYPES)

            case "GTS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 == Types.NIL or type2 == Types.NIL:
                    Errors.Exit(Errors.RUN_TYPES)
                if type1 == type2:
                    if symb1 > symb2: 
                        self.data_stack.append([True, Types.BOOL])
                    else:
                        self.data_stack.append([False, Types.BOOL])
                else:
                    Errors.Exit(Errors.RUN_TYPES)

            case "ANDS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 != Types.BOOL or type2 != Types.BOOL:
                    Errors.Exit(Errors.RUN_TYPES)
                self.data_stack.append([symb1 and symb2, Types.BOOL])

            case "ORS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 != Types.BOOL or type2 != Types.BOOL:
                    Errors.Exit(Errors.RUN_TYPES)
                self.data_stack.append([symb1 or symb2, Types.BOOL])

            case "NOTS":
                if len(self.data_stack) < 1:
                    Errors.Exit(Errors.RUN_VALMISS)
                data = self.data_stack.pop()
                if data[1] != Types.BOOL:
                    Errors.Exit(Errors.RUN_TYPES)
                self.data_stack.append([not data[0], Types.BOOL])

            case "INT2CHARS":
                if len(self.data_stack) < 1:
                    Errors.Exit(Errors.RUN_VALMISS)
                data = self.data_stack.pop()
                if data[1] != Types.INT:
                    Errors.Exit(Errors.RUN_TYPES)
                try:
                    self.data_stack.append([chr(data[0]), Types.STRING])
                except:
                    Errors.Exit(Errors.RUN_STRING)

            case "STRI2INTS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 != Types.STRING or type2 != Types.INT:
                    Errors.Exit(Errors.RUN_TYPES)
                if len(symb1) <= symb2 or symb2 < 0:
                    Errors.Exit(Errors.RUN_STRING)
                else:
                    self.data_stack.append([ord(symb1[symb2]), Types.INT])

            case "JUMPIFEQS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 == type2:
                    if symb1 == symb2: 
                        return code.labels[arg1]
                elif type1 == Types.NIL or type2 == Types.NIL:
                    return None
                else:
                    Errors.Exit(Errors.RUN_TYPES)

            case "JUMPIFNEQS":
                symb1, symb2, type1, type2 = self.__stack_get2values()
                if type1 == type2:
                    if symb1 != symb2: 
                        return code.labels[arg1]
                elif type1 == Types.NIL or type2 == Types.NIL:
                    return code.labels[arg1]
                else:
                    Errors.Exit(Errors.RUN_TYPES)

            case _:
                Errors.Exit(Errors.INTERNAL)

        return None


    # získá první 2 hodnoty na vrcholu zásobníku, které musí být typu INT
    def __stack_get2ints(self):
        if len(self.data_stack) < 2:
            Errors.Exit(Errors.RUN_VALMISS)
        data = self.data_stack.pop()
        if data[1] != Types.INT:
            Errors.Exit(Errors.RUN_TYPES)
        symb2 = data[0]
        data = self.data_stack.pop()
        if data[1] != Types.INT:
            Errors.Exit(Errors.RUN_TYPES)
        symb1 = data[0]
        return symb1, symb2
    
    # získá první 2 položky (hodnota + typ) na vrcholu zásobníku 
    def __stack_get2values(self):
        if len(self.data_stack) < 2:
            Errors.Exit(Errors.RUN_VALMISS)
        data = self.data_stack.pop()
        type2 = data[1]
        symb2 = data[0]
        data = self.data_stack.pop()
        type1 = data[1]
        symb1 = data[0]
        return symb1, symb2, type1, type2

    # přesune data proměnných z 1 rámce do proměnných ve 2. rámci
    def changeFrame(self, frameOld, symtable, old = "local"):
        frameNew = []
        prefix = "TF"
        if(old != "local"):
            prefix = "LF"
        if len(frameOld) > 0:
            for var in frameOld:
                ret = symtable.FindToken(prefix + var.identif[2:], Types.VAR)
                if ret != None:
                    self.copyDataVar(var, ret)
                    frameNew.append(ret)
                var.defined = False
        return frameNew

    # zkopíruje obsah proměnných
    def copyDataVar(self, old, new):
        new.data = old.data
        new.data_type = old.data_type
        new.defined = True
        old.defined = False

    # uloží aktuální hodnoty lokálního rámce (z důvodu shody identifikátorů)
    def SaveLocalFrameData(self):
        backup = {}
        if len(self.local_frame) > 0:
            for var in self.local_frame[len(self.local_frame)-1]:
                backup[var] = [var.data, var.IsDefined(), var.data_type]
        self.local_frame_backup.append(backup)

    # vrátí uložené hodnoty zpět do přslušných proměnných
    def RestoreLocalFrameData(self):
        if len(self.local_frame_backup) < 1:
            return
        backup = self.local_frame_backup.pop()
        if len(self.local_frame) < 1:
            return
        for var in self.local_frame[len(self.local_frame)-1]:
            var.data = backup[var][0]
            var.defined = backup[var][1]
            var.data_type = backup[var][2]
