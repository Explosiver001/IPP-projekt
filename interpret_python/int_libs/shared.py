import sys

class Errors:
    XML_WF = 31
    XML_STRUCT = 32
    SEM = 52
    RUN_TYPES = 53
    RUN_VAR = 54
    RUN_NOTEX = 55
    RUN_VALMISS = 56
    RUN_OPVAL = 57
    RUN_STRING = 58   
    INTERNAL = 99
    messages = {
                XML_WF: "chybny XML format ve vstupnim souboru",
                XML_STRUCT: "neocekavana struktura XML",
                SEM: "chyba pri semantickych kontrolach vstupniho kodu v IPPcode23 (napr. pouziti nedefinovaneho navesti, redefinice promenne)",
                RUN_TYPES: "behova chyba interpretace – spatne typy operandu",
                RUN_VAR: "behova chyba interpretace – pristup k neexistujici promenne (ramec existuje)",
                RUN_NOTEX :"behova chyba interpretace – ramec neexistuje (napr. cteni z prazdneho zasobniku ramcu)",
                RUN_VALMISS :"behova chyba interpretace – chybejici hodnota (v promenne, na datovem zasobniku nebov zasobniku volani)",
                RUN_OPVAL :"behova chyba interpretace – spatna hodnota operandu (napr. deleni nulou, spatna navra-tova hodnota instrukce EXIT)",
                RUN_STRING :"behova chyba interpretace – chybna prace s retezcem"
    }
    
    def Exit(code, message = None, file = None):
        if file != None:
            file.close()
        if message == None:
            if code != Errors.INTERNAL:
                message = Errors.messages[code]
            else:
                message = "vnitrni chyba interpretu"
        sys.stderr.write(message+"\n")
        exit(code)