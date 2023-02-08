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

}


function read_lines($input_file){
    while(!feof($input_file)){
        $line = fgets($input_file);
        $split_line = explode(' ', $line);
        if(is_instruction($split_line[0])){
            echo $split_line[0] . "\n";
        }
    }
}




?>