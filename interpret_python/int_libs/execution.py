from .scanner import *
import copy

PC_stack = []
data_stack = []
global_frame = []
local_frame = []
temporal_frame = []

def Execute(instruction, labels, line):
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
            if not arg1.isDefined() or not arg2.isDefined():
                print("ERROR MOVE")
            else:
                arg1.data = arg2.data
                arg1.data_type = arg2.data_type
        case "CREATEFRAME":
            temporal_frame = []
        case "PUSHFRAME":
            #local_frame.append(temporal_frame) #! +-
            return None
        case "POPFRAME":
            #temporal_frame = local_frame.pop() #! +-
            return None
        case "DEFVAR":
            if arg1.isDefined():
                print("ERROR DEFVAR")
            else:
                arg1.defineVar()
                if str.find(arg1.identif, "GF@") != -1:
                    global_frame.append(arg1)
                elif str.find(arg1.identif, "LF@") != -1:
                    local_frame.append(arg1)
                elif str.find(arg1.identif, "TF@") != -1:
                    temporal_frame.append(arg1)
        case "CALL":
            print("HERE")
        case "RETURN":
            print("HERE")
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
            print("HERE")
        case "SUB":
            print("HERE")
        case "MUL":
            print("HERE")
        case "IDIV":
            print("HERE")
        case "LT":
            print("HERE")
        case "GT":
            print("HERE")
        case "EQ":
            print("HERE")
        case "AND":
            print("HERE")
        case "OR":
            print("HERE")
        case "NOT":
            print("HERE")
        case "INT2CHAR":
            print("HERE")
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
            if not checkVarsDefinitions(arg1, arg2, arg3):
                print("ERROR CONCAT")
            else:
                arg1.data = arg2.data + arg3.data
        case "STRLEN":
            print("HERE")
        case "GETCHAR":
            print("HERE")
        case "SETCHAR":
            print("HERE")
        case "TYPE":
            print("HERE")
        case "LABEL":
            return None
        case "JUMP":
            return labels[arg1]
        case "JUMPIFEQ":
            if arg2.data_type is arg3.data_type and arg3.data == arg2.data: 
                return labels[arg1]
            if arg2.data_type is Types.NIL or arg3.data_type is Types.NIL:
                return labels[arg1]

        case "JUMPIFNEQ":
            print("HERE")
        case "EXIT":
            print("HERE")
        case "DPRINT":
            print("HERE")
        case "BREAK":
            print("HERE")
        case _:
            print("ERROR")

def checkVarsDefinitions(arg1, arg2, arg3):
    def1 = True if arg1 is None else arg1.isDefined()
    def2 = True if arg2 is None else arg2.isDefined()
    def3 = True if arg3 is None else arg3.isDefined()
    return (def1 and def2 and def3)