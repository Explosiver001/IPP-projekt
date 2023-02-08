<?php
include 'vars.php';



function is_instruction($token){
    global $instruction_set;
    foreach($instruction_set as $instruction){
        if (!strcmp($instruction, $token))
            return true;
    }
    return false;
}

function is_operand($token){
    $variable_pattern = "/^((LF)|(TF)|(GF))@([-]|[a-z]|[A-Z]|[0-9]|[_$&%*!?])*$/";
    $string_pattern = "/^string@$/"; //TODO fix
    $int_pattern = "/^(int@[+-]\d+)|(int@\d+)$/";
    $bool_pattern = "/^(bool@true)|(bool@false)$/";
    $nil_pattern = "/^nil@nil$/";



    if (preg_match($variable_pattern, $token) || preg_match($string_pattern, $token) || preg_match($int_pattern, $token) 
        || preg_match($bool_pattern, $token) || preg_match($nil_pattern, $token))
        return true;
    return false;
}


function read_lines($input_file){
    global $stderr;
    while(!feof($input_file)){
        $in_comment = false;
        $line = fgets($input_file);
        $line = trim($line);
        $split_line = explode(' ', $line);

        for ($i = 0; $i < count($split_line); $i++) {
            if (!$in_comment) {
                if (!strcmp($split_line[$i], "#")) { // komnetáře
                    $in_comment = true;
                }
                elseif (!(is_operand($split_line[$i]) || is_instruction($split_line[$i]))){ // token není instrukce ani operand
                    fprintf($stderr, "<< %s >> neni validni token!\n\n", $split_line[$i]);
                }
                else{
                    fprintf($stderr, "(( %s )) je validni token!\n\n", $split_line[$i]);
                }
                    
            }
        }
    }
}

?>