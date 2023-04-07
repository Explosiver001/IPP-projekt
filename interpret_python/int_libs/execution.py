#
# soubor:   execution.py
# autor:    Michal Novák <xnovak3>  
#   

from .scanner import *
from .resources import *

class Runner:
    def __init__(self, input):
        self.input = input
        self.PC_stack = []
        self.data_stack = []
        self.local_frame = []
        self.local_frame_backup = []
        self.temporal_frame = []
        self.createFrame = False
        self.instructionsPreformed = 0

    def ReadInput(self):
        if self.input == None:
            str = input()
            return str
        else:
            str = self.input.readline()
            str = str.rstrip("\n")
            return str

    def GetLocalFrame(self):
        return self.local_frame
    
    def GetTemporalFrame(self):
        return self.temporal_frame, self.createFrame

    def ExecuteInstruction(self, instruction, code, line):
        opcode = instruction[0]
        
        arg1 = None
        arg2 = None
        arg3 = None
        if len(instruction) >= 4:
            arg3 = instruction[3]
        if len(instruction) >= 3:
            arg2 = instruction[2]
        if len(instruction) >= 2:
            arg1 = instruction[1]
        
        self.instructionsPreformed += 1
        
        match opcode.identif:
            case "MOVE":
                arg1.data = arg2.data
                arg1.data_type = arg2.data_type
                
            case "CREATEFRAME":
                self.createFrame = True
                self.temporal_frame = []
                
            case "PUSHFRAME":
                if self.createFrame == False:
                    Errors.Exit(Errors.RUN_NOTEX, file=self.input)
                self.SaveLocalFrameData()
                if len (self.local_frame) > 0:
                    for var in self.local_frame[len(self.local_frame)-1]:
                        var.data = None
                        var.defined = False
                self.local_frame.append(self.changeFrame(self.temporal_frame, code.symtable, "temporal")) 
                self.createFrame = False
                
            case "POPFRAME":
                if(len(self.local_frame) <= 0):
                    Errors.Exit(Errors.RUN_NOTEX, file=self.input)
                self.temporal_frame = self.changeFrame(self.local_frame.pop(), code.symtable, "local")
                self.RestoreLocalFrameData()
                self.createFrame = True
                
            case "DEFVAR":
                arg1.DefineVar()
                if str.find(arg1.identif, "LF@") != -1:
                    self.local_frame[len(self.local_frame)-1].append(arg1)
                elif str.find(arg1.identif, "TF@") != -1:
                    self.temporal_frame.append(arg1)
                
            case "CALL":
                if arg1 not in code.labels:
                    Errors.Exit(Errors.SEM, file=self.input)
                self.PC_stack.append(line)
                return code.labels[arg1]
            
            case "RETURN":          
                if len(self.PC_stack) > 0:
                    ret = self.PC_stack.pop()
                    return ret + 1
                else:
                    
                    Errors.Exit(Errors.RUN_VALMISS, file=self.input)
            case "PUSHS":
                self.data_stack.append(arg1.data)
                self.data_stack.append(arg1.data_type)
                
            case "POPS":
                if len(self.data_stack) != 0:
                    arg1.data_type = self.data_stack.pop()
                    arg1.data = self.data_stack.pop()
                else:
                    Errors.Exit(Errors.RUN_VALMISS, file=self.input)
                    
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
                    Errors.Exit(Errors.RUN_OPVAL, file=self.input)
                    
            case "LT":
                arg1.data_type = Types.BOOL
                arg1.data = (arg2.data < arg3.data)
                
            case "GT":
                arg1.data_type = Types.BOOL
                arg1.data = (arg2.data > arg3.data)
                
            case "EQ":
                arg1.data_type = Types.BOOL
                arg1.data = (arg2.data == arg3.data)
                
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
                try:
                    arg1.data = chr(arg2.data)
                except:
                    Errors.Exit(Errors.RUN_STRING, file=self.input)

            case "STRI2INT":
                if len(arg2.data) <= arg3.data or arg3.data < 0:
                    Errors.Exit(Errors.RUN_STRING, file=self.input)
                else:
                    arg1.data = ord(arg2.data[arg3.data])
                    arg1.data_type = Types.INT
                    
            case "READ":
                try:
                    data = self.ReadInput()
                    arg1.ChangeDataType(Scanner.GetType(arg2.identif))
                    if arg1.ChangeData(data) == False:
                        raise EOFError
                except EOFError:
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
                    Errors.Exit(Errors.RUN_STRING, file=self.input)
                    
            case "SETCHAR":
                if arg1.data_type != Types.STRING:
                    Errors.Exit(Errors.RUN_TYPES, file=self.input)
                if arg3.data == "":
                    Errors.Exit(Errors.RUN_STRING, file=self.input)
                if len(arg1.data) > arg2.data and arg2.data >= 0:
                    string = arg1.data
                    arg1.data = string[0:arg2.data] + arg3.data[0] + string[arg2.data+1:]    
                else:
                    Errors.Exit(Errors.RUN_STRING, file=self.input)
                    
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
                    Errors.Exit(Errors.SEM, file=self.input)
                return code.labels[arg1]
            
            case "JUMPIFEQ":
                if arg1 not in code.labels:
                    Errors.Exit(Errors.SEM, file=self.input)
                if arg2.data_type is arg3.data_type:
                    if arg3.data == arg2.data: 
                        return code.labels[arg1]
                elif arg2.data_type is Types.NIL or arg3.data_type is Types.NIL:
                    if arg3.data == arg2.data: 
                        return code.labels[arg1]
                else:
                    Errors.Exit(Errors.RUN_TYPES, file=self.input)
                    
            case "JUMPIFNEQ":
                if arg1 not in code.labels:
                    Errors.Exit(Errors.SEM, file=self.input)
                if arg2.data_type is arg3.data_type:
                    if arg3.data != arg2.data: 
                        return code.labels[arg1]
                elif arg2.data_type is Types.NIL or arg3.data_type is Types.NIL:
                    if arg3.data != arg2.data: 
                        return code.labels[arg1]
                else:
                    Errors.Exit(Errors.RUN_TYPES, file=self.input)
                    
            case "EXIT":
                if arg1.data >= 0 and arg1.data <= 49:
                    exit(arg1.data)
                else:
                    Errors.Exit(Errors.RUN_OPVAL, file=self.input)
                
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

            case _:
                Errors.Exit(Errors.INTERNAL)
                
                
        return None

    def checkVarsDefinitions(arg1, arg2, arg3):
        def1 = True if arg1 is None else arg1.isDefined()
        def2 = True if arg2 is None else arg2.isDefined()
        def3 = True if arg3 is None else arg3.isDefined()
        return (def1 and def2 and def3)

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
        
    def copyDataVar(self, old, new):
        new.data = old.data
        new.data_type = old.data_type
        new.defined = True
        old.defined = False
    
    def SaveLocalFrameData(self):
        backup = {}
        if len(self.local_frame) > 0:
            for var in self.local_frame[len(self.local_frame)-1]:
                backup[var] = [var.data, var.IsDefined(), var.data_type]
        self.local_frame_backup.append(backup)
        
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
        