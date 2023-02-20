from .scanner import *

PC_stack = []

def Execute(instruction, labels, line):
    opcode = instruction[0]
    #print("{",opcode.identif, opcode.type,"}") ##!debug
    match opcode.identif:
        case "MOVE":
            print("HERE")
        case "CREATEFRAME":
            print("HERE")
        case "PUSHFRAME":
            print("HERE")
        case "POPFRAME":
            print("HERE")
        case "DEFVAR":
            print("HERE")
        case "CALL":
            print("HERE")
        case "RETURN":
            print("HERE")
        case "PUSHS":
            print("HERE")
        case "POPS":
            print("HERE")
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
            print("HERE")
        case "READ":
            print("HERE")
        case "WRITE":
            print("HERE")
        case "CONCAT":
            print("HERE")
        case "STRLEN":
            print("HERE")
        case "GETCHAR":
            print("HERE")
        case "SETCHAR":
            print("HERE")
        case "TYPE":
            print("HERE")
        case "LABEL":
            print("HERE")
        case "JUMP":
            print("HERE")
        case "JUMPIFEQ":
            print("HERE")
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
            
def Move(arg1, arg2):
    arg1.data = arg2.data

#def Createframe():

#def Pushframe():

#def Createframe():

#def Popframe():

def Defvar(var):
    var.defineVar()

#def Call():