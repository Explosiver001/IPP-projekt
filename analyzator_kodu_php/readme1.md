Implementační dokumentace k 1. úloze do IPP 2022/2023
Jméno a příjmení: Michal Novák
Login: xnovak3g

# Základní struktura projektu

Projekt se skládá ze 4 hlavních částí:
- Hlavní spouštěč `parse.php`
- Lexikální analýza `parse_libs/scanner.php`
- Syntaktická analýza `parse_libs/parser.php`
- Generátor mezikódu `parse_libs/generator.php`

## 1) Hlavní spouštěč 
Provádí zpracování argumentů příkazové řádky a volání jednotlivých komponent analýzy kódu.
Na zpracování argumentů byla použita knihovna **getopt**, povolené argumenty jsou: `-h` a `--help`.

## 2) Lexikální analýza
Načítá vstupní kód v jazyce IPPcode23 a vyhodnocuje lexikální správnost. Kód je načítán po jednotlivých řádcích a postupně zpracováván. Načtený řádek se upraví tak, aby bylo možné jej rozdělit do pole, které obsahuje celé instrukce a jejich operandy. Dále je pomocí regulárních výrazů zjištěn typ a nalezeny případné lexikální chyby. Pokud je lexikální analýza, vrací se 2D pole obsahující zpracovaný vstup v následujícím formátu:
| index 	| 0                        	| 1                        	| 2                        	| 3                        	|
|-------	|--------------------------	|--------------------------	|--------------------------	|--------------------------	|
| 0     	| {"DEFVAR", Instruction}  	| {"GF@a", Var}            	|                          	|                          	|
| 1     	| {"ADD", Instruction}     	| {"GF@a",Var}             	| {"10", Int}              	| {"Hello", String}        	|
| 2     	| {"READ", Instruction}    	| {"GF@a", Var}            	| {"bool",Type}            	|                          	|
| n     	| {[Identifikator], [typ]} 	| {[Identifikator], [typ]} 	| {[Identifikator], [typ]} 	| {[Identifikator], [typ]} 	|

## 3) Syntaktická analýza
Je založena na tabulce pravidel pro jazyk IPPcode23. Tabulka obsahuje údaje o počtu a typu proměnných pro jednotlivé instrukce. 

Sémantická analýza je v této části kontrolována jen okrajově. 

## 4) Generátor mezikódu
Vnitřní reprezentace kódu IPPcode23 je pomocí knihovny XMLWriter převedena do formátu XML, který je vypsán na standardní výstup.