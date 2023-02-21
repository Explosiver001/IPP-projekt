import sys

class Errors:
    SEM = 52
    RUN_TYPES = 53
    RUN_VAR = 54
    RUN_NOTEX = 55
    RUN_VALMISS = 56
    RUN_OPVAL = 57
    RUN_STRING = 58   
    messages = [
                "chyba pri semantickych kontrolach vstupniho kodu v IPPcode23 (napr. pouziti nedefinovaneho navesti, redefinice promenne)",
                "behova chyba interpretace – spatne typy operandu",
                "behova chyba interpretace – pristup k neexistujici promenne (ramec existuje)",
                "behova chyba interpretace – ramec neexistuje (napr. cteni z prazdneho zasobniku ramcu)",
                "behova chyba interpretace – chybejici hodnota (v promenne, na datovem zasobniku nebov zasobniku volani)",
                "behova chyba interpretace – spatna hodnota operandu (napr. deleni nulou, spatna navra-tova hodnota instrukce EXIT)",
                "behova chyba interpretace – chybna prace s retezcem"
    ]
    
    def Exit(code, message = None):
        if message == None:
            message = Errors.messages[code-Errors.SEM]
        sys.stderr.write(message+"\n")
        exit(code)