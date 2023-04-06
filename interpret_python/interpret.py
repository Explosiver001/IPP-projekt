import getopt, sys

from int_libs import scanner as S
from int_libs import parser as P
from int_libs import execution as E
from int_libs import shared

def main():
    source_file = sys.stdin
    input_file = None
    
    long_options=["help", "source=", "input="]
    short_options="h"
    opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    for opt in opts:
        if opt[0] == "--help" or opt[0] == "-h":
            print("Zprava")
            exit(0)
        if opt[0] == "--input":
            input_file = opt[1]
        if opt[0] == "--source":
            source_file = opt[1]

    # print("Source: ", source_file)
    # print("Input: ", input_file, "\n")
    
    code = S.get_tokens(source_file)
    if len(code.lines) == 0:
        sys.exit(0)
    
    if input_file != None:
        try:
            input_file = open(input_file, "r")
        except:
            shared.Erros.Exit(shared.Errors.INTERNAL, message="--input soubor se nepodarilo otevrit")
    
    
    runner = E.Runner(input_file)
    analyzer = P.Parser()
    
    PC = 0 # program counter
    while PC <= max(code.lines.keys()) :
        if PC in code.lines.keys():
            instr = code.lines[PC]
            analyzer.Analyze(instr, runner)
            ret = runner.ExecuteInstruction(instr, code, PC)
            if ret is None:
                PC += 1
            else:
                PC = ret
        else:
            PC += 1
    
    if input_file != None:
        input_file.close()



if __name__ == "__main__":
    main()