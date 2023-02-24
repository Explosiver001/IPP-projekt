from .scanner import *
from .shared import *
import copy

PC_stack = []
data_stack = []
local_frame = []
temporal_frame = []

def Execute(instruction, code, line):
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
    match opcode.identif:
        
        case "MOVE":
            arg1.data = arg2.data
            arg1.data_type = arg2.data_type
            
        case "CREATEFRAME":
            temporal_frame = []
            
        case "PUSHFRAME":
            local_frame.append(changeFrame(temporal_frame, code.symtable, "temporal")) #! +-
            
        case "POPFRAME":
            temporal_frame = changeFrame(local_frame.pop(), code.symtable, "local")
            
        case "DEFVAR":
            arg1.defineVar()
            if str.find(arg1.identif, "LF@") != -1:
                local_frame.append(arg1)
            elif str.find(arg1.identif, "TF@") != -1:
                temporal_frame.append(arg1)
                
        case "CALL":
            return code.labels[arg1]
        
        case "RETURN":
            if len(PC_stack) >= 0:
                ret = PC_stack.pop()
                return ret
            else:
                print("ERROR RETURN")
            
        case "PUSHS":
            data_stack.append(arg1.data)
            data_stack.append(arg1.data_type)
            
        case "POPS":
            if len(data_stack) != 0:
                arg1.data_type = data_stack.pop()
                arg1.data = data_stack.pop()
            else:
                print("ERROR POPS")
                
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
                print("ERROR 57")
                
        case "LT":
            print("HERE")
            
        case "GT":
            print("HERE")
            
        case "EQ":
            print("HERE")
            
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
                print("ERROR 58")

        case "STRI2INT":
            if len(arg2.data) >= arg3.data:
                print("ERROR STRI2INT")
            elif not arg1.isDefined():
                print("ERROR STRI2INT")
            else:
                arg1.data = ord(arg2.data[arg3.data])
                
        case "READ":
            data = input()
            arg1.changeDataType(GetType(arg2.identif))
            print(arg2.identif)
            arg1.changeData(data)
            
        case "WRITE":
            if arg1.data_type is Types.NIL:
                print("",end="")
            elif arg1.data_type is Types.BOOL:
                if arg1.data is True:
                    print("true", end="")
                else:
                    print("false", end="")
            else:
                print(arg1.data, end="")
                
        case "CONCAT":
            arg1.data = arg2.data + arg3.data
            
        case "STRLEN":
            arg1.data_type = Types.INT
            arg1.data = len(arg2.data)
                
        case "GETCHAR":
            arg1.data_type = Types.STRING
            if len(arg2.data) > arg3.data and arg3.data >= 0:
                arg1.data = arg2.data[arg3.data]
            else:
                print("ERROR 53")
                
        case "SETCHAR":
            if len(arg1.data) > arg2.data and arg2.data >= 0:
                arg1.data[arg2.data] = arg3.data[0]   
            else:
                print("ERROR 53")
                
        case "TYPE":
            arg1.data_type = Types.STRING
            match arg2.data_type:
                case Types.INT:
                    arg1.data = "int"
                case Types.STRING:
                    arg1.data = "string"
                case Types.BOOL:
                    arg1.data = "bool"
                case Types.NIL:
                    arg1.data = "nil"
                    
        case "LABEL":
            return None
        
        case "JUMP":
            return code.labels[arg1]
        
        case "JUMPIFEQ":
            if arg2.data_type is arg3.data_type:
                if arg3.data == arg2.data: 
                    return code.labels[arg1]
            elif arg2.data_type is Types.NIL or arg3.data_type is Types.NIL:
                return code.labels[arg1]
            else:
                print("ERROR 53")
                
        case "JUMPIFNEQ":
            if arg2.data_type is arg3.data_type:
                if arg3.data != arg2.data: 
                    return code.labels[arg1]
            elif arg2.data_type is Types.NIL or arg3.data_type is Types.NIL:
                return code.labels[arg1]
            else:
                print("ERROR 53")
                
        case "EXIT":
            print("HERE")
            
        case "DPRINT":
            print("HERE")
            
        case "BREAK":
            print("HERE")
            
        case _:
            print("ERROR")
            
            
    return None

def checkVarsDefinitions(arg1, arg2, arg3):
    def1 = True if arg1 is None else arg1.isDefined()
    def2 = True if arg2 is None else arg2.isDefined()
    def3 = True if arg3 is None else arg3.isDefined()
    return (def1 and def2 and def3)

def changeFrame(frameOld, symtable, old = "local"):
    frameNew = []
    prefix = "LF"
    if(old != "local"):
        prefix = "TF"
    for var in frameOld:
        ret = symtable.findToken(var.identif)
        if ret != None:
            copyDataVar(var, ret)
            frameNew.append(ret)
    return frameNew
    
def copyDataVar(old, new):
    new.data = old.data
    new.data_type = new.data_type
    new.defined = True
    old.defined = False