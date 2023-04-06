from .scanner import *
from .execution import *
from .shared import *


INS_ARG_COUNT = {
    0: ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"],
    1: ["DEFVAR", "POPS", "CALL", "PUSHS", "WRITE", "DPRINT", "LABEL", "JUMP", "EXIT"],
    2: ["MOVE", "NOT", "INT2CHAR", "READ", "STRLEN", "TYPE"],
    3: ["ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "CONCAT", "AND", "OR", "STRI2INT", "GETCHAR", "SETCHAR", "JUMPIFEQ", "JUMPIFNEQ"]
}

RULE_SET = [
    [["MOVE"],
        [Types.VAR, False], 
        [Types.SYMBOL, True]],
    [["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]],
    [["DEFVAR"], 
        [Types.VAR, False]],
    [["POPS"], 
        [Types.VAR, False]],
    [["CALL"], 
        [Types.LABEL, False]],
    [["PUSHS"], 
        [Types.SYMBOL, True]],
    [["ADD", "SUB", "MUL", "IDIV"], 
        [Types.VAR, False], 
        [Types.INT, True], 
        [Types.INT, True]],
    [["LT", "GT", "EQ"], 
        [Types.VAR, False], 
        [Types.INT, True], 
        [Types.INT, True]],
    [["LT", "GT", "EQ"], 
        [Types.VAR, False], 
        [Types.BOOL, True], 
        [Types.BOOL,True]],
    [["EQ"], 
        [Types.VAR, False], 
        [Types.NIL, True], 
        [Types.SYMBOL,True]],
    [["EQ"], 
        [Types.VAR, False], 
        [Types.SYMBOL, True], 
        [Types.NIL,True]],
    [["EQ"], 
        [Types.VAR, False], 
        [Types.NIL, True], 
        [Types.NIL,True]],
    [["LT", "GT", "EQ", "CONCAT"], 
        [Types.VAR, False], 
        [Types.STRING, True], 
        [Types.STRING, True]],   
    [["AND", "OR"], 
        [Types.VAR, False], 
        [Types.BOOL, True], 
        [Types.BOOL, True]],
    [["NOT"], 
        [Types.VAR, False], 
        [Types.BOOL, True]],
    [["INT2CHAR"], 
        [Types.VAR, False], 
        [Types.INT, True]],
    [["STRI2INT", "GETCHAR"],
        [Types.VAR, False],
        [Types.STRING, True],
        [Types.INT, True]],
    [["READ"],
        [Types.VAR, False],
        [Types.TYPE, True]],
    [["WRITE", "DPRINT"],
        [Types.SYMBOL, True]],
    [["STRLEN"],
        [Types.VAR, False],
        [Types.STRING, True]],
    [["SETCHAR"],
        [Types.VAR, True],
        [Types.INT, True],
        [Types.STRING, True]],
    [["TYPE"],
        [Types.VAR, False],
        [Types.SYMBOL, True]],
    [["LABEL", "JUMP"],
        [Types.LABEL, False]],
    [["JUMPIFEQ", "JUMPIFNEQ"],
        [Types.LABEL, False],
        [Types.SYMBOL, True],
        [Types.SYMBOL, True]],
    [["EXIT"],
        [Types.INT, True]],
]

class Parser:
    def Analyze(self, instruction, runner):
        localframe = runner.GetLocalFrame()
        temporalframe, createfame =  runner.GetTemporalFrame()
        self.CheckDefinition(instruction, localframe, temporalframe, createfame)
        self.CheckSem(instruction)
            
    def CheckSem(self, instruction):
        opcode = instruction[0]

        for argCount in INS_ARG_COUNT:
            if argCount == len(instruction)-1:
                if opcode.identif not in INS_ARG_COUNT[argCount]:
                    Errors.Exit(Errors.XML_STRUCT)
        
        for rule in RULE_SET:
            
            if opcode.identif in rule[0]:
                matchFound = True
                # print(rule)
                if len(rule) != len(instruction):
                    matchFound = False
                else:
                    for i in range(1, len(rule)):
                        arg = instruction[i]
                        if rule[i][1] == True and arg.type == Types.VAR and arg.data == None and arg.data_type != Types.NIL:
                            Errors.Exit(Errors.RUN_VALMISS)
                            break
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
                        if (rule[i][0] == Types.INT or rule[i][0] == Types.BOOL or rule[i][0] == Types.STRING or rule[i][0] == Types.NIL) and arg.data_type != rule[i][0]: 
                            matchFound = False
                            break
                if not matchFound and rule[0] != ["LT", "GT", "EQ"]:
                    Errors.Exit(Errors.RUN_TYPES)
                elif matchFound:
                    return True
        Errors.Exit(Errors.SEM, None)
                


    def CheckDefinition(self, instruction, localframe, temporalframe, createFrame):
        opcode = instruction[0]

        for j in range(1, len(instruction)):
            arg = instruction[j]

            if arg.type == Types.VAR and opcode.identif == "DEFVAR":
                if arg.isDefined():
                    Errors.Exit(Errors.SEM)
                if "TF@" in arg.identif:
                    if not createFrame:
                        Errors.Exit(Errors.RUN_NOTEX)
                elif "LF@" in arg.identif:
                    if len(localframe) < 1:
                        Errors.Exit(Errors.RUN_NOTEX)
            if arg.type == Types.VAR and opcode.identif != "DEFVAR":
                if "TF@" in arg.identif:
                    if not createFrame:
                        Errors.Exit(Errors.RUN_NOTEX)
                    if not arg.isDefined():
                        Errors.Exit(Errors.RUN_VAR)
                    if arg not in temporalframe:
                        Errors.Exit(Errors.RUN_NOTEX)
                elif "LF@" in arg.identif:
                    if len(localframe) < 1:
                        Errors.Exit(Errors.RUN_NOTEX)
                    if not arg.isDefined():
                        Errors.Exit(Errors.RUN_VAR) 
                    if arg not in localframe[len(localframe)-1]:
                        Errors.Exit(Errors.RUN_NOTEX)
                elif "GF@" in arg.identif:
                    if not arg.isDefined():
                        Errors.Exit(Errors.RUN_VAR)

