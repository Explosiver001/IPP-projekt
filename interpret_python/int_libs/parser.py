from .scanner import *
from .execution import *


#!USELESS
#RULE_SET = [
#    [["MOVE"],
#        Types.VAR, 
#        Types.SYMBOL],
#    [["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN"]],
#    [["DEFVAR", "POPS"], 
#        Types.VAR],
#    [["CALL"], 
#        Types.LABEL],
#    [["PUSHS"], 
#        Types.SYMBOL],
#    [["ADD", "SUB", "MUL", "IDIV"], 
#        Types.VAR, 
#        Types.INT, 
#        Types.INT],
#    [["LT", "GT", "EQ"], 
#        Types.VAR, 
#        Types.INT, 
#        Types.INT],
#    [["LT", "GT", "EQ"], 
#        Types.VAR, 
#        Types.BOOL, 
#        Types.BOOL],
#    [["LT", "GT", "EQ", "CONCAT"], 
#        Types.VAR, 
#        Types.STRING, 
#        Types.STRING],   
#    [["AND", "OR"], 
#        Types.VAR, 
#        Types.BOOL, 
#        Types.BOOL],
#    [["NOT"], 
#        Types.VAR, 
#        Types.BOOL],
#    [["INT2CHAR"], 
#        Types.VAR, 
#        Types.INT]
#    [["STRI2INT", "GETCHAR"],
#        Types.VAR,
#        Types.STRING,
#        Types.INT],
#    [["READ"],
#        Types.VAR,
#        Types.TYPE],
#    [["WRITE"],
#        Types.SYMBOL],
#    [["STRLEN"],
#        Types.VAR,
#        Types.STRING],
#    [["SETCHAR"],
#        Types.VAR,
#        Types.INT,
#        Types.STRING],
#    [["TYPE"],
#        Types.VAR,
#        Types.SYMBOL],
#    [["LABEL", "JUMP"],
#        Types.LABEL],
#    
#]



def analyze_and_execute(code):
    PC = 0 # program counter
    while PC < len(code.lines):
        instr = code.lines[PC]
        ret = Execute(instr, code.labels, PC)
        if ret is None:
            PC += 1
        else:
            PC = ret




