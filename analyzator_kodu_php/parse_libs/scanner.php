<?php
include_once 'vars.php';



function is_instruction($token){
    global $instruction_set;
    foreach($instruction_set as $instruction){
        if (!strcmp(strtolower($instruction), strtolower($token)))
            return true;
    }
    return false;
}

function find_type($token){
    // regulární výrazy pro povolené tokeny
    $variable_pattern = "/^((LF)|(TF)|(GF))@([-]|[a-z]|[A-Z]|[_$&%*!?])([-]|[a-z]|[A-Z]|[0-9]|[_$&%*!?])*$/";
    //$string_pattern = "/^string@([!\"]|[%-[]|]|\^|[_-~]|([\\\\][0-9][0-9][0-9]))*$/"; //! stara verze, jen ascii 0-127
    $string_pattern = "/^string@(([^\#\\\\\001-\032])|([\\\\][0-9][0-9][0-9]))*$/";
    $int_pattern = "/^(int@[+-]\d+)|(int@\d+)$/";
    $bool_pattern = "/^(bool@true)|(bool@false)$/";
    $nil_pattern = "/^nil@nil$/";
    $type_pattern = "/^(int)|(string)|(bool)$/";
    $label_pattern = "/^([-]|[a-z]|[A-Z]|[_$&%*!?])([-]|[a-z]|[A-Z]|[0-9]|[_$&%*!?])*$/";
    $comment_pattern = "/^#/";
    $header_pattern = "/^.IPPcode23$/";

    // zjištění jednotlivých typů
    if(is_instruction($token))
        return Types::Instruction;
    if(preg_match($header_pattern, $token))
        return Types::Header;
    if(preg_match($comment_pattern, $token))
        return Types::Comment;
    if(preg_match($variable_pattern, $token))
        return Types::Var;
    if(preg_match($int_pattern, $token))
        return Types::Int;
    if(preg_match($bool_pattern, $token))
        return Types::Bool;
    if(preg_match($string_pattern, $token))
        return Types::String;
    if(preg_match($nil_pattern, $token))
        return Types::Nil;
    if(preg_match($type_pattern, $token))
        return Types::Type;
    if(preg_match($label_pattern, $token))
        return Types::Label;

    // token nebyl rozpoznán
    return Types::Error;
}

// funkce lexikální analýzy + uložení tokenů
function scanner($input_file): array{
    global $stderr; // chybový výstup
    global $DEBUG_PARAM; 

    $code_array = array(); // výstupní data
    // čtení souboru
    while(!feof($input_file)){ 
        $line = fgets($input_file); // načtení řádku

        // zpracování řádku do jednodušší podoby
        $line = str_replace("#", " #", $line); // před komentářem je vždy mezera
        $line = str_replace("# ", "#", $line);
        while(str_contains($line, "\t") || str_contains($line, "  ")){ // odebrání veškerých dvoj-mezer a tabelátorů
            $to_replace = array("  ", "\t");
            $line = str_replace($to_replace, " ", $line);
        }

        $line = trim($line); // odebrání bílých znaků ze začátku a konce řádku

        // ošetření prázdných řádků
        if(!strcmp($line, "")){ 
            continue;
        }
        
        $split_line = explode(' ', $line); // rozdělení řádku do pole
        $operation = array(); // výsledný zpracovaný řádek == instrukce + operandy

        for ($i = 0; $i < count($split_line); $i++) {
            $ret_type = find_type($split_line[$i]); // zjištění typu
            if($ret_type == Types::Comment) // v případě komentáře se ukončí zpracování řádku
                break;
            elseif($i == 0 && $ret_type != Types::Instruction && $ret_type != Types::Header){ // lehká invaze ze syntakticé analýzy, nerozpoznaná instrukce
                if(empty($code_array)){
                    fprintf($stderr, "ERROR:: chyba hlavicky %s\n", $split_line[$i]);
                    exit(Header_Error);
                }
                
                fprintf($stderr, "ERROR:: neznama instrukce %s\n", $split_line[$i]);
                exit(UnknownCode_Error);
            }
            elseif($ret_type == Types::Error){ // chyba
                fprintf($stderr, "ERROR:: neznamy operand %s\n", $split_line[$i]);
                exit(LexSyn_Error);
            }
            else{ // token je operand
                $token = new Token($split_line[$i], $ret_type);
                array_push($operation, $token);
            }
        }
        if(!empty($operation)) // prázdný řádek není předán dál
            array_push($code_array, $operation); // přidání zpracovaného řádku pro další operace
    }

    if($DEBUG_PARAM) // pomocný výpis
        print_r($code_array);

    return $code_array; 
}

?>