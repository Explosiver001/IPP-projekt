from .scanner import *
from .execution import *
from .shared import *

#!USELESS
RULE_SET = [
    [["MOVE"],
        [Types.VAR,     True], 
        [Types.SYMBOL,  True]],
    [["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]],
    [["DEFVAR"], 
        [Types.VAR,     False]],
    [["POPS"], 
        [Types.VAR,     True]],
    [["CALL"], 
        [Types.LABEL,   True]],
    [["PUSHS"], 
        [Types.SYMBOL,  True]],
    [["ADD", "SUB", "MUL", "IDIV"], 
        [Types.VAR,     True], 
        [Types.INT,     True], 
        [Types.INT,     True]],
    [["LT", "GT", "EQ"], 
        [Types.VAR,     True], 
        [Types.INT,     True], 
        [Types.INT,     True]],
    [["LT", "GT", "EQ"], 
        [Types.VAR,     True], 
        [Types.BOOL,    True], 
        [Types.BOOL,    True]],
    [["LT", "GT", "EQ", "CONCAT"], 
        [Types.VAR,     True], 
        [Types.STRING,  True], 
        [Types.STRING,  True]],   
    [["AND", "OR"], 
        [Types.VAR,     True], 
        [Types.BOOL,    True], 
        [Types.BOOL,    True]],
    [["NOT"], 
        [Types.VAR,     True], 
        [Types.BOOL,    True]],
    [["INT2CHAR"], 
        [Types.VAR,     True], 
        [Types.INT,     True]],
    [["STRI2INT", "GETCHAR"],
        [Types.VAR,     True],
        [Types.STRING,  True],
        [Types.INT,     True]],
    [["READ"],
        [Types.VAR,     True],
        [Types.TYPE,    True]],
    [["WRITE", "DPRINT"],
        [Types.SYMBOL,  True]],
    [["STRLEN"],
        [Types.VAR,     True],
        [Types.STRING,  True]],
    [["SETCHAR"],
        [Types.VAR,     True],
        [Types.INT,     True],
        [Types.STRING,  True]],
    [["TYPE"],
        [Types.VAR,     True],
        [Types.SYMBOL,  True]],
    [["LABEL", "JUMP"],
        [Types.LABEL,   True]],
    [["JUMPIFEQ", "JUMPIFNEQ"],
        [Types.LABEL,   True],
        [Types.SYMBOL,  True],
        [Types.SYMBOL,  True]],
    [["JUMPIFEQ", "JUMPIFNEQ"],
        [Types.LABEL,   True],
        [Types.SYMBOL,  True],
        [Types.SYMBOL,  True]],
    [["EXIT"],
        [Types.INT,     True]],
]


def analyze_and_execute(code):
    PC = 0 # program counter
    while PC < len(code.lines):
        #input("INSTR: "+code.lines[PC][0].identif)
        if not checkSem(code.lines[PC]):
            print("ERROR:", PC)
        instr = code.lines[PC]
        ret = Execute(instr, code, PC)
        if ret is None:
            PC += 1
        else:
            PC = ret
            
        
def checkSem(instruction):
    opcode = instruction[0]
    for rule in RULE_SET:
        if opcode.identif in rule[0]:
            matchFound = True
            if len(rule) != len(instruction):
                matchFound = False
            else:
                for i in range(1, len(rule)):
                    arg = instruction[i]
                    if rule[i][0] == Types.VAR and arg.type != Types.VAR:
                        matchFound = False
                        break
                    if rule[i][0] == Types.SYMBOL and not arg.isSymbol():
                        matchFound = False
                        break
                    if rule[i][0] == Types.LABEL and arg.type != Types.LABEL:
                        matchFound = False
                        break
                    if rule[i][0] == Types.TYPE and arg.type != Types.TYPE:
                        matchFound = False
                        break
                    if (rule[i][0] == Types.INT or rule[i][0] == Types.BOOL or rule[i][0] == Types.STRING) and arg.data_type != rule[i][0]: 
                        matchFound = False
                        break
                    if rule[i][1] != arg.isDefined():
                        matchFound = False
                        break
            if not matchFound:
                print("ERROR", opcode.identif)
            else:
                return True
    Errors.Exit(Errors.SEM, None)
            



