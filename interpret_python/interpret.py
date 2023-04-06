import getopt, sys

from int_libs.scanner import Scanner
from int_libs.parser import Parser
from int_libs.execution import Runner
from int_libs import resources


class Interpret:
    def __init__(self, source_file, input_file):
        self.source_file = source_file
        self.input_file = input_file
    
    def Start(self):
        code = Scanner.GetTokens(self.source_file) # získání kódu z XML soubo+ sourceru
        if len(code.lines) == 0: # kód je prázdný
            sys.exit(0)

        if self.input_file != None:
            try:
                self.input_file = open(self.input_file, "r")
            except:
                resources.Erros.Exit(resources.Errors.INTERNAL, message="--input soubor se nepodarilo otevrit")

        runner = Runner(self.input_file) # inicializace 
        
        PC = 0 # Programový čítač (umístění v programu)
        while PC <= max(code.lines.keys()) :
            if PC in code.lines.keys():
                instr = code.lines[PC]
                Parser.Analyze(instr, runner)
                ret = runner.ExecuteInstruction(instr, code, PC)
                if ret is None:
                    PC += 1
                else:
                    PC = ret
            else:
                PC += 1
                
        if self.input_file != None:
            self.input_file.close()




def main():
    source_file = sys.stdin
    input_file = None
    
    optionUsed = False
    
    long_options=["help", "source=", "input="]
    short_options="h"
    opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    for opt in opts:
        if opt[0] == "--help" or opt[0] == "-h":
            print("Zprava")
            exit(0)
        if opt[0] == "--input":
            optionUsed = True
            input_file = opt[1]
        if opt[0] == "--source":
            optionUsed = True
            source_file = opt[1]

    if not optionUsed:
        resources.Errors.Exit(resources.Errors.INTERNAL, message="Musi byt pouzit alespon 1 z prepinacu --input --source")
        
    interpret = Interpret(source_file, input_file)
    interpret.Start()



if __name__ == "__main__":
    main()