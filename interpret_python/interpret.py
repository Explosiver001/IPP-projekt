#
# soubor:   interpret.py
# autor:    Michal Novák <xnovak3g>  
# Vstupní bod interpretu. Zpracovávají se zde argumenty příkazové řádky. Dále se zde řídí a spojuje chod celého interpretu
#

import getopt, sys

from int_libs.scanner import Scanner
from int_libs.parser import Parser
from int_libs.execution import Runner
from int_libs import resources

# třída propojující jednotlivé části interpretu
class Interpret:
    def __init__(self, source_file, input_file):
        self.source_file = source_file
        self.input_file = input_file
    
    # spouští chod interpretu
    def Start(self):
        code = Scanner.GetTokens(self.source_file) # získání kódu z XML souboru
        if len(code.lines) == 0: # kód je prázdný
            sys.exit(0)
        if self.input_file != None:
            try:
                self.input_file = open(self.input_file, "r")
            except:
                resources.Erros.Exit(resources.Errors.INTERNAL, message="--input soubor se nepodarilo otevrit")

        runner = Runner(self.input_file) # inicializace 
        
        # uzavření souboru s uživatelskými vstupy (vstupy jsou již uloženy interně)
        if self.input_file != None:
            self.input_file.close()
        
        PC = 0 # Programový čítač (umístění v programu)
        while PC <= max(code.lines.keys()) :
            if PC in code.lines.keys(): 
                instr = code.lines[PC]
                ret = Parser.Analyze(instr, runner) # syntaktická a sémantická analýza
                if ret != 0:
                    resources.Errors.Exit(ret)
                ret = runner.ExecuteInstruction(instr, code, PC) # vykonání instrukce
                if ret is None: 
                    PC += 1
                else:
                    PC = ret
            else: # přeskočení chybějících pořadí
                PC += 1




# zpracování argumentů příkazové řádky a spuštění interpretace
def main():
    source_file = sys.stdin # soubor s kódem
    input_file = None # soubor s uživatelskými vstupy (pokud None, použije se STDIN)
    
    optionUsed = False
    
    long_options=["help", "source=", "input="]
    short_options="h"
    opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    for opt in opts:
        if opt[0] == "--help" or opt[0] == "-h":
            print("Interpret jazyka IPPcode23 ulozeneho v XML reprezentaci. Verze pro python 3.10.\nMoznosti pri spusteni:\n\t--help, -h\tVypise tuto zpravu\n\t--input=file\tNastavi file jako uzivatelsky vstup\n\t--source=file\tNastavi file jako vstup zdrojoveho kodu\nAlespon jeden z prepinacu --input a --source musi byt pouzit")
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



# vstupní bod programu
if __name__ == "__main__":
    main()